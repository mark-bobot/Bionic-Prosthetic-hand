# EMG mounting and cable fit

**Layout defined; physical fit and wearer site unverified.** Retain current CAD until hardware and wearer measurements justify edits.

The SEN0240 has two boards: conditioner inside the housing; dry electrode against exposed skin on an independently adjustable band. Neither the skin-contact site nor band tension can be finalised from a generic arm cylinder.

## Conditioner inside the box

Bottom-drive CAD places the reference at X = 21 mm, Y = −93 mm, Z = 8–43 mm in local box coordinates. The 22 × 35 mm PCB stands upright with a 10 mm thickness allowance, beside the Nano. Inspect the actual jack orientation, components, plug and lead bend before mounting.

- Use existing carrier tie slots with insulating backing and removable retention. No new hole pattern is assumed.
- Avoid pressure on components and retain access to unplug the probe with power off.
- The right-side entry is nominally 8 mm diameter at Y = −93 mm, Z = 30 mm. Select an actual grommet and check assembly access; the connector may need threading before board installation.
- Check cables throughout hand travel and unpowered cover removal. Keep ties/leads clear of drum grooves and structural motor seats.
- Record dimensions and photos of the board, plug, grommet, backing and lead bend. Envelope tests cannot replace these measurements.

## Electrode outside the carrier

DFRobot lists a 22 × 35 mm electrode and supplied 50 cm lead. Placement guidance calls for exposed skin and alignment with muscle direction. [Specifications](https://wiki.dfrobot.com/sen0240/) · [Placement reference](https://wiki.dfrobot.com/sen0240/docs/20735)

The intended site is the open underside between arm straps, **provided a prosthetist confirms usable muscle, socket pressure and suspension permit it**. Strap centres Y = −142 and −57 mm are CAD coordinates, not an anatomical prescription. If the suitable site is elsewhere, reposition the independent band or revise the prescribed interface.

Use a removable adjustable band and insulated backing with all intended metal contacts exposed. Measure contact projection: a guessed printed rim can lift the contacts off skin. Band material, width, padding and retention remain wearer-specific. Avoid hard connectors under loaded straps. Strain-relieve the cable on the band with movement slack that cannot snag.

## Before any worn sensor trial

On an arm-shaped fixture, check adjustment, unobstructed contacts, insulation, retention, jack loading and access. Establish cleaning and skin-contact material suitability with the supplier/fitting professional. This verifies assembly only, not skin tolerance or signal quality.

The fitting professional must establish muscle site, orientation, contact quality, adjustment and skin checks before connecting a person. Do not prescribe pressure from CAD or tighten until the signal improves. Electrode loss can still produce a plausible signal; this single-channel controller cannot reliably detect it.

The first reviewed body-connected assessment, if approved, should have all motor plugs physically removed and output-disabled firmware. Sensor-only work is still a human test; this document does not authorise it. Powered fitting requires a separate later decision after [bench and release verification](PRE-HUMAN-TEST.md).
