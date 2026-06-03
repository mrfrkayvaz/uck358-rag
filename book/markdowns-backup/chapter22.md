# *Challenge of Stealth Aerodynamics*

The invention of aircraft that are almost invisible to ground or surface-to-airmissile radars promises to be an effective defensive measure for reconnaissance and attack airplanes. This development has taken six paths so far, the first three of which are a distinct challenge to stability and control designers:

- **Faceted airframes** replace the smooth aerodynamic shapes that produce attached flows and linear aerodynamics. Radar returns from faceted shapes, such as the Lockheed F-117A, are absent except for the instants when a facet faces the radar transmitter.
- **Parallel-line planforms** have the same sweep angle on wing leading and trailing edges and on surface tips and sharp edges. Parallel-line planforms concentrate radar returns into narrow zones that are easily missed by search radars. This is the Northrop B-2 stealth method, augmented by special materials and buried engines.
- **Suppressed vertical tails** are either shielded from radar by wing structure or eliminated altogether. The Lockheed F-22 has shielded vertical tails, the B-2 none at all.
- **Blended aerodynamics** eliminate internal cornerssuch aswing–fuselage intersections. Internal corners can act as radar corner reflectors. The Rockwell B-1 usesthistechnique to reduce itsradar signature.
- **Buried engines and exhausts** hide compressor fan blades and hot exhaust pipes from radar and infrared seekers.
- **Radar-absorbent materials** are used, generally nonmetallic. Thisisa highly classified subject.

The challenges of faceted airframes, parallel-line planforms, and suppressed vertical tails to stability and control engineers are illustrated by current stealth airplanes.

## **22.1 Faceted Airframe Issues**

The Lockheed F-117A'sfaceted airframe fliesin the face of conventional aerodynamic wisdom, which requires smooth surfaces to maintain attached flow under the widest possible ranges of angles of attack, sideslip, and angular velocities (Figure 22.1). On the other hand, the aerodynamic forcesand momentsof faceted airframesare reasonably linear functions of these variables for sufficiently small ranges.

Large-wing sweepback, 67 1/2 degreesin the case of the F-117A, extendsthe linear rangessomewhat, making facet edgesinto side edgesinstead of breaksnormal to the flow direction. Still, the stability and control engineer who is faced with a faceted airframe such as the F-117A must expect to restrict flight parameters in order to avoid nonlinear and unstable aerodynamic moments that exceed available control power. The F-117A was originally called "The Hopeless Diamond" by Lockheed aerodynamicists.

![Chapter 22 - Figure 1](../assets/chapter22/_page_1_Figure_1.jpeg)

**Figure 22.1** Faceted structure of the Lockheed F-117A Stealth Fighter. (From Lockheed Advanced Development Company, J. W. Ragsdale)

On the F-117A, the angle of attack is hard-limited, but sideslip angles are unlimited with the landing gear down for cross-wind landings. With landing gear up, the sideslip angle is nulled by closed-loop control, a normal loop closure. F-117A longitudinal static margins are low or negative within the angle-of-attack limit range, but air combat maneuverscan be made within that range. Severe pitchupsand pitchdownsoccur outside of the angle-of-attack limit range (Farley and Abrams, 1990). Without augmentation, the airplane is directionally unstable over large partsof itsoperational envelope.

The four F-117A elevonshave relatively large travelsof 60 degreesup and down, which are necessary to deal with nonlinear and unstable moments within the angle-of-attack limit range. The two vertical tails are all-moving, for the same reason. The F-117A has quadruple fail-safe fly-by-wire controls, using F-16 technology. An 18-foot-diameter braking parachute doubles as a spin chute, an unusual feature for a service airplane. Nominal landing speed is 160 knots, at an angle of attack of 9 1/2 degrees.

#### **22.2 Parallel-Line Planform Issues**

The Northrop B-2 planform strongly distorts from the ideal the additional span load distributions, or the span loadings due to symmetric angle of attack and to rolling. Each planform internal corner, marked "C" in Figure 22.2, producesa sharp local peak in the additional span loading, as do the triangle-shaped wing tips. Premature stalling can be expected in the vicinity of the cornersat high anglesof attack and at high rolling velocities.

The resultant nonlinearity in the variation of lift with angle of attack at high angles is not in itself a stability and control problem. However, the yawing and rolling moment due to rolling derivatives *Cn <sup>p</sup>* and *C*<sup>l</sup> *<sup>p</sup>* , normally negative in sign, become positive at combined high angle-of-attack and rolling velocity values. Thisproblem iscountered in the B-2 with an angle-of-attack limiter and with artificial stability increments that are tailored to *Cn <sup>p</sup>* and *C*<sup>l</sup>*<sup>p</sup>* valuesbelow the angle-of-attack limits.

![Chapter 22 - Figure 1](../assets/chapter22/_page_2_Picture_5.jpeg)

**Figure 22.2** Internal sharp corners, marked "C" on the Northrop B-2 bomber planform. These corners, the result of the stealth parallel-line planform, produce sharp local peaks in the wing's additional spanload distribution. Premature stalling can be expected in the vicinity of the corners at high angles of attack and rolling velocities.

A second B-2 stability and control issue is the elimination of vertical tails, requiring split ailerons to supply yawing moments in response to pilot and autopilot inputs. The split aileronsact asdifferential drag devices. The brake drag, and hence yawing moment, isnonlinear with brake opening, requiring further tailoring to produce predictable control moments.

As with all isolated sweptback wings, the B-2 has an inherent low level of positive static directional stability. However, the sweptback hinge lines of the split ailerons result in directional instability whenever the brakes are opened symmetrically at large angles, asan airspeed-control device. The open brakesthemselvesact aslow-aspect-ratio wings, with lift componentsthat produce destabilizing yawing momentswhen the whole wing is yawed to the airstream. The speed brakes are opened at landing approach airspeeds, putting an additional requirement on the logic that providesartificial directional stability at low airspeeds.

In addition to a very small level of inherent static directional stability, the B-2's all-wing shape has next to no side force derivative in sideslip, or *Cy*<sup>β</sup> . Thiscreatesa flight instrument problem, in that the normal ball-bank component of the turn and slip instrument cannot function as an indication of airplane sideslip. The standard ball-bank component is a lateral accelerometer, calibrated to produce one ball width at a tilt angle of 4.5 degrees, or a lateral acceleration of 0.08 g, in level flight. With virtually no side force developed in sideslip, there is no lateral acceleration to displace the ball. This instrumentation problem is aside from flight dynamicsproblemsthat occur with essentially zero *Cy*<sup>β</sup> .

The Northrop B-2 wasthe very first parallel-planform configuration to be built. Engineers who were willing to talk about its development concede that there were some unpleasant stability and control surprises. Radar signature considerations probably rule out alleviation of distortions in span load by local wing twist for future applications. Correction for undesirable (positive in sign) values of *Cn <sup>p</sup>* by artificial stability increments is of course available with sophisticated digital flight control systems, but the amount of correction available islimited for configurationswithout vertical tails. Thisisbecause the rudder power, or ability to generate yawing moments, is small for split aileron controls as compared with conventional vertical tail surfaces.

### **22.3 Shielded Vertical Tails and Leading-Edge Flaps**

Radar return from an airplane'sbottom isan important consideration if the airplane isto operate where hostile ground radarsrather than air- or space-borne radarsare the major defense. Intersections of vertical tails with wing or fuselage surfaces act as corner reflectors, increasing radar returns. This is the reason why vertical tails are located entirely above wing surfaceson airplanessuch asthe Lockheed F-117A and F-22 (Figure 22.3).

Vertical surface shielding from radar by above-wing mountings has the undesirable effect of shielding the vertical surfaces from the airflow at large positive angles of attack. Premature departuresinto uncontrolled flight and spinsresult. Canting vertical tail tipsoutward, ason the F-117A and F-22 designs, is intended to put at least the tail tips out in unshielded flow at large positive angles of attack.

The importance of radar returnsfrom an airplane'sbottom wasbrought out by Fulghum (1994). He reported that some reduction in the number of underwing doors, access panels, and drain holeswasrequired to lower radar returnsfrom the F-22. Radar returnsfrom seams or junctures between fixed and movable surfaces are another consideration. Leadingedge flaps in particular are a cause of concern because of the lower seam between the flap and wing. The F-22 isequipped with leading-edge flaps. The F-22'sleading-edge flaps

![Chapter 22 - Figure 1](../assets/chapter22/_page_4_Picture_0.jpeg)

**Figure 22.3** The Lockheed F-22, showing its vertical tail intersections with the wings that are shielded from ground radars. The vertical tail tips are canted outward to retain some effectiveness at high angles of attack. (From Lockheed Martin Corporation)

![Chapter 22 - Figure 1](../assets/chapter22/_page_4_Picture_2.jpeg)

**Figure 22.4** NASA 8-Ft. Transonic Wind-Tunnel model of a U.S. Air Force Multirole fighter concept, designed to have no vertical tail. Directional stability and control would be provided by thrust vectoring and low-radar-return control surfaces. (NASA photo 93–01934)

are an important contributor to the airplane'sair combat capability, including itsreported ability to fly stably at an angle of attack of 60 degrees. Leading- and trailing-edge flaps are programmed with Mach number and angle of attack to maintain lateral and directional stability.

#### **22.4 Fighters Without Vertical Tails**

The designers of the B-2 stealth bomber proved that the stability and control requirements for a subsonic-level bomber can be met without vertical tails. What is not clear is whether the more severe fighter stability and control requirements can be met without vertical tails.

All designs in a USAF Wright Laboratory multirole fighter study have either small vertical tailsor none at all (Figure 22.4) (Oliveri, 1994). The preferred replacement for normal vertical tails is thrust vectoring and split ailerons. These controls were used successfully on the NASA/Boeing X-36 Fighter Agility Research Aircraft. A 28-percent-scale remotely piloted model wasflown in 1997, reaching an angle of attack of 40 degrees.

A thrust vectoring scheme used to replace fighter vertical tails must have a highbandwidth actuator responding to sideslip signals for directional stability as well as other stability-augmentation system signals and commands from the pilot. Unless split ailerons are used, for safety reasons it would seem necessary for a thrust vectoring sideslip loop to provide directional stability even at idle thrust. Alternately, engine thrust could be diverted left and right when idle thrust is needed and modulated for directional stability and control.

All in all, stability and control engineers should come well prepared at design meetings where stealth is the topic.