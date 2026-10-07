"""Regression checks for unit/landmark errors and false fit claims."""
from pathlib import Path
import copy, json, sys, unittest
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'cad/sizing'))
from sizing import evaluate, validate

class SizingTests(unittest.TestCase):
    def setUp(self):
        self.p=json.loads((R/'cad/sizing/profile.json').read_text())
        self.b={'wrist_to_middle_tip_mm':137,'palm_section_width_mm':60,'palm_section_y_mm':60}
    def test_unknown_is_not_a_fit(self):
        r=evaluate(self.p,self.b)
        self.assertFalse(r['patient_fit_verified'])
        self.assertEqual(r['length_check']['status'],'MEASUREMENTS_REQUIRED')
        self.assertIsNone(r['servo_gravity_moment_about_elbow_Nm'])
    def test_scale_preserves_proportion_not_hardware_interface(self):
        r=evaluate(self.p,self.b)
        self.assertAlmostEqual(r['projected_cad_wrist_to_middle_tip_mm'],164.4)
        self.assertAlmostEqual(r['palm_section_width_mm'],72)
        self.assertFalse(r['existing_receiver_matches_hand_scale'])
    def test_registered_wrist_offset_sign(self):
        # Synthetic unit-test dimensions only; CAD wrist 10 mm distal to anatomy.
        self.p['measurements'].update(elbow_to_opposite_wrist_mm=300,elbow_to_residual_tip_mm=200,cad_wrist_distal_to_anatomical_wrist_mm=10,opposite_hand_length_mm=175)
        r=evaluate(self.p,self.b)
        self.assertEqual(r['length_check']['available_residual_tip_to_cad_wrist_mm'],110)
        self.assertEqual(r['length_check']['existing_package_extra_length_mm'],50)
        self.assertAlmostEqual(r['hand_proportion_check']['length_difference_mm'],-.6)
        self.assertAlmostEqual(r['servo_gravity_moment_about_elbow_Nm'],.0676*9.80665*(182+192+182)/1000)
    def test_shorter_desired_gap_does_not_shrink_hardware(self):
        self.p['limb_clearance_envelope']['distal_end_y_mm']=-80
        r=evaluate(self.p,self.b)
        self.assertEqual(r['required_existing_package_residual_tip_to_cad_wrist_mm'],160)
        self.assertEqual(r['design_residual_tip_to_cad_wrist_mm'],80)
    def test_different_width_and_length_are_not_averaged(self):
        self.p['measurements'].update(opposite_hand_length_mm=164.4,cad_wrist_distal_to_anatomical_wrist_mm=0,cad_palm_width_target_mm=90)
        r=evaluate(self.p,self.b)['hand_proportion_check']
        self.assertAlmostEqual(r['length_only_scale_percent'],120)
        self.assertAlmostEqual(r['width_only_scale_percent'],150)
    def test_enlarged_hand_can_exceed_fixed_spool_travel(self):
        self.p['measurements']['baseline_hand_only_closure_travel_mm']=27
        r=evaluate(self.p,self.b)
        self.assertEqual(r['travel_screen']['status'],'INSUFFICIENT_IDEAL_TRAVEL')
        self.p['hand_scale_percent']=100
        self.assertEqual(evaluate(self.p,self.b)['travel_screen']['status'],'IDEAL_TRAVEL_ONLY')
    def test_bad_profile_fails(self):
        for value in [False,0,-1,float('inf'),'120']:
            p=copy.deepcopy(self.p);p['hand_scale_percent']=value
            with self.assertRaises(ValueError):validate(p)
        self.p['limb_clearance_envelope']['distal_end_y_mm']=-350
        with self.assertRaises(ValueError):validate(self.p)

if __name__=='__main__':unittest.main()
