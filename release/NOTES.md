# Prototype 0.2 — integrated right bionic CAD

Download the ZIP and start with `BUILD.md`. This revision adds a connected thumb fork, fixed palm receiver, two-part residual-forearm shell with EMG access, guided equaliser cassette, thumb slider, liner guide comb and a lid with dedicated liner entries. The original Phoenix palm and finger shapes are retained. STEP/STL exports, parametric sources, current print/hardware lists, wiring, force calculations and simple 32-sample EMG averaging firmware are included.

New printable parts pass valid-solid and watertight STL checks. Static assembly collision checks, 18 sampled equaliser poses and sampled thumb-root positions pass. Nano firmware compiles (7,228 bytes flash, 653 bytes global RAM) with AVR core 1.8.8 and Servo 1.3.0. Host control and actual-filter integration tests pass using synthetic inputs.

**Pre-release for bench development.** Socket dimensions and several bought-part outlines remain assumptions. Axle/fastener fit, flexible-line installation, full articulation, structural retention, actual force/EMG/noise/thermal testing and individual socket/suspension fitting remain acceptance gates. No powered-wear approval or historical-performance proof is claimed. The drive cassette increases height above the previous bare housing.
