"""Sizing arithmetic, independent of CAD. Units: mm, g, N m. CC BY 4.0."""
import math

MEASUREMENTS = (
    'elbow_to_opposite_wrist_mm', 'elbow_to_residual_tip_mm',
    'cad_wrist_distal_to_anatomical_wrist_mm', 'elbow_to_socket_opening_mm',
    'opposite_hand_length_mm', 'cad_palm_width_target_mm',
    'baseline_hand_only_closure_travel_mm',
)

def number(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{name} must be a finite number')
    if positive and value <= 0:
        raise ValueError(f'{name} must be greater than zero')
    return float(value)


def validate(profile):
    number(profile['hand_scale_percent'], 'hand_scale_percent', True)
    scales = profile['comparison_scales_percent']
    if not isinstance(scales, list) or not 1 <= len(scales) <= 5:
        raise ValueError('Use one to five comparison scales')
    for s in scales:
        number(s, 'comparison scale', True)
    e = profile['limb_clearance_envelope']
    for k in ['opening_y_mm', 'distal_end_y_mm', 'axis_z_mm']:
        number(e[k], k)
    if not e['opening_y_mm'] < e['distal_end_y_mm'] < 0:
        raise ValueError('Envelope must run from opening to distal end, behind CAD wrist Y=0')
    for k in ['proximal_width_mm', 'proximal_depth_mm', 'distal_width_mm', 'distal_depth_mm']:
        number(e[k], k, True)
    m = profile['measurements']
    for k in MEASUREMENTS:
        if m.get(k) is not None:
            number(m[k], k, positive=k != 'cad_wrist_distal_to_anatomical_wrist_mm')
    if m.get('elbow_to_residual_tip_mm') is not None and m.get('elbow_to_socket_opening_mm') is not None:
        if m['elbow_to_socket_opening_mm'] >= m['elbow_to_residual_tip_mm']:
            raise ValueError('Socket opening must be proximal to residual tip')
    return profile


def evaluate(profile, baseline):
    validate(profile)
    s = profile['hand_scale_percent'] / 100
    e, m = profile['limb_clearance_envelope'], profile['measurements']
    result = {
        'status': 'DESIGN_STUDY_NOT_FITTED',
        'hand_scale_percent': s * 100,
        'projected_cad_wrist_to_middle_tip_mm': baseline['wrist_to_middle_tip_mm'] * s,
        'palm_section_width_mm': baseline['palm_section_width_mm'] * s,
        'palm_section_y_mm': baseline['palm_section_y_mm'] * s,
        'socket_engagement_design_mm': e['distal_end_y_mm'] - e['opening_y_mm'],
        'design_residual_tip_to_cad_wrist_mm': -e['distal_end_y_mm'],
        'required_existing_package_residual_tip_to_cad_wrist_mm': 160,
        'existing_receiver_matches_hand_scale': math.isclose(s, 1, abs_tol=1e-9),
        'patient_fit_verified': False,
        'unknown_measurements': [k for k in MEASUREMENTS if m.get(k) is None],
        'length_check': {'status': 'MEASUREMENTS_REQUIRED'},
        'socket_engagement_check': {'status': 'MEASUREMENTS_REQUIRED'},
        'hand_proportion_check': {},
        'servo_mass_only_g': 3 * 67.6,
        'servo_mass_only_tolerance_g': 3.0,
        'servo_gravity_moment_about_elbow_Nm': None,
    }
    if all(m.get(k) is not None for k in ['elbow_to_opposite_wrist_mm', 'elbow_to_residual_tip_mm', 'cad_wrist_distal_to_anatomical_wrist_mm']):
        elbow_to_cad = m['elbow_to_opposite_wrist_mm'] + m['cad_wrist_distal_to_anatomical_wrist_mm']
        gap = elbow_to_cad - m['elbow_to_residual_tip_mm']
        result['length_check'] = {
            'status': 'EXISTING_PACKAGE_TOO_LONG' if gap < 160 else 'AXIAL_SPACE_ONLY',
            'available_residual_tip_to_cad_wrist_mm': gap,
            'existing_package_extra_length_mm': max(0, 160 - gap),
            'envelope_distal_end_alignment_error_mm':  -e['distal_end_y_mm'] - gap,
        }
        # Candidate case centres used as mass-centre approximations; horizontal arm.
        result['servo_gravity_moment_about_elbow_Nm'] = 67.6 / 1000 * 9.80665 * sum(
            abs(elbow_to_cad + y) / 1000 for y in [-128, -118, -128])
    if all(m.get(k) is not None for k in ['elbow_to_socket_opening_mm', 'elbow_to_residual_tip_mm']):
        available = m['elbow_to_residual_tip_mm'] - m['elbow_to_socket_opening_mm']
        result['socket_engagement_check'] = {
            'status': 'GEOMETRIC_COMPARISON_ONLY',
            'measured_opening_to_tip_mm': available,
            'design_minus_measured_mm': result['socket_engagement_design_mm'] - available,
        }
    # Hand length is comparable only after registering mechanical and anatomical datums.
    if m.get('opposite_hand_length_mm') is not None and m.get('cad_wrist_distal_to_anatomical_wrist_mm') is not None:
        offset = m['cad_wrist_distal_to_anatomical_wrist_mm']
        candidate = result['projected_cad_wrist_to_middle_tip_mm'] + offset
        result['hand_proportion_check']['length_difference_mm'] = candidate - m['opposite_hand_length_mm']
        result['hand_proportion_check']['length_only_scale_percent'] = 100 * (m['opposite_hand_length_mm'] - offset) / baseline['wrist_to_middle_tip_mm']
    if m.get('cad_palm_width_target_mm') is not None:
        result['hand_proportion_check']['width_difference_mm'] = result['palm_section_width_mm'] - m['cad_palm_width_target_mm']
        result['hand_proportion_check']['width_only_scale_percent'] = 100 * m['cad_palm_width_target_mm'] / baseline['palm_section_width_mm']
    # Fixed spool and assumed sweep from current candidate; not an actual measured stroke.
    takeup = 12.3 * math.radians(160)
    result['travel_screen'] = {
        'scope': 'Hand-only similarity estimate. Fixed routing, return bands and friction must be measured again.',
        'assumed_spool_radius_mm': 12.3, 'assumed_sweep_degrees': 160,
        'ideal_takeup_mm': takeup, 'assumed_slack_allowance_mm': 3,
        'max_baseline_hand_only_stroke_mm_at_selected_scale': (takeup - 3) / s,
        'status': 'MEASUREMENT_REQUIRED',
    }
    if m.get('baseline_hand_only_closure_travel_mm') is not None:
        travel = m['baseline_hand_only_closure_travel_mm'] * s
        result['travel_screen'].update({
            'estimated_scaled_hand_only_stroke_mm': travel,
            'status': 'INSUFFICIENT_IDEAL_TRAVEL' if travel + 3 > takeup else 'IDEAL_TRAVEL_ONLY',
        })
    return result
