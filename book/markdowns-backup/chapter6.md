# *Stability and Control at the Design Stage*

In the preliminary layout of a new airplane, the stability and control engineer isgenerally guided by some well-known principlesrelated to balance and tail sizing, for example. Once a preliminary design is laid out, its main stability and control characteristics can be predicted entirely from drawings. This includes the neutral point (center of gravity for zero-static longitudinal stability), static directional (weathercock) and lateral (dihedral effect) stability, and assurance that the airplane can be trimmed to zero-pitching moment over itslift coefficient and center of gravity ranges.

In the best of circumstances, the new design has a family resemblance to an earlier design. Then the estimations resemble extrapolations from known, measured characteristics. All airplane manufacturersseem to maintain proprietary aerodynamic handbook collections and correlations of stability and control data from previous designs. This is a great help if the extrapolation route is indicated. Aside from these private collections, there is a large body of theory and correlationsfrom generalized wind-tunnel data that can be called upon for prediction or estimation.

A closely related subject to the prediction of stability and control characteristics entirely from drawingsisthe problem posed at the next stage in an airplane'sdevelopment, when wind-tunnel test data have been obtained. In former times, one was often asked to prepare a complete set of predicted flying qualities using the wind-tunnel data and any flight control detailsthat may have been available at the time. Instead, current practice isto plug windtunnel test and control system data into a flight simulator, for pilot flying qualities evaluation. Radio-controlled flying scale models are an alternate stability and control source for projects that cannot afford wind-tunnel tests.

The three design-stage topics – layout principles, estimation from drawings, and estimation from wind-tunnel data – are treated in thischapter.

## **6.1 Layout Principles**

## **6.1.1** *Subsonic Airplane Balance*

Subsonic tail-last (not canard) airplanes are generally balanced to bring their centersof gravity near the wing-alone aerodynamic center. Thisisthe point at which the wing's pitching moment coefficient isinvariant with angle of attack. For reasonably high wing aspect ratios, the wing-alone aerodynamic center is near the 25-percent point behind the leading edge of chord line passing through the wing's center of area. This chord line is called the wing'smean aerodynamic chord or mac. Figure 6.1 showsthe simple geometric construction defining the mac for straight-tapered and elliptical wings.

Tailless airplanes must have their centers of gravity ahead of the wing aerodynamic center or 25-percent mac point to be inherently statically stable. If the wing is swept back, it can be trimmed at a reasonably high lift coefficient with trailing-edge-up deflections of its elevons. The degree of static stability desired and the maximum lift coefficient obtained are interrelated. Taillessairplanescan have their centersof gravity behind the wing

![Chapter 6 - Figure 1](../assets/chapter6/_page_1_Figure_1.jpeg)

**Figure 6.1** Geometrical constructions for the mean aerodynamic chord (mac) on straight-tapered and elliptical wings.

aerodynamic center if static stability is provided by artificial means or stability augmentation (see Chapter 20). Longitudinal trim then requirestrailing-edge-down elevon. Thisincreases effective wing camber, with beneficial effectson performance (Ashkenasand Klyde, 1989).

The canard configuration, abandoned after 1910 by its inventors, the Wright brothers, hasbeen revived in recent years, notably by Burt Rutan, in the belief that the arrangement provides natural stall prevention (see Chapter 17, Sec. 2). Also, trimming with an upload isthought to reduce induced drag, although thishasbeen disputed. The neutral point, or center of gravity for neutral stability, of canard airplanes is considerably ahead of the 25-percent point of the wing mac. On the Rutan machines, fuel tanks are fitted in triangular leading-edge extensionsto keep the fuel near the airplane'scenter of gravity.

## **6.1.2** *Tail Location, Size, and Shape*

Horizontal and vertical tails are commonly located about a wing semispan behind the center of gravity. While horizontal tail sizes normally range from 15 to 30 percent of the wing area, the actual size is a complex function of desired center of gravity range, ground effect, and other factors. There is a minimum tail size that will trim a neutrally stable airplane at maximum lift in ground effect. Horizontal tails that are larger than this absolute minimum permit a useful operational center of gravity range.

Optimization theory has been proposed to size horizontal tails for particular center of gravity ranges, considering actuator rate and amplitude and flying qualities constraints. A particular application (Kaminer, Howard, and Buttrill, 1997) starts with a particular horizontal tail volume. Then, the most aft center of gravity location and feedback gains are found that (1) put longitudinal short-period eigenvalues into a region of MIL-STD 1797 Level 1 or 2 flying qualitiesand (2) do not exceed actuator rate or amplitude limits in response to a severe vertical gust. The problem as stated has reasonable solutions. The method, although involved, may be useful in preliminary design.

There seems to be no upper limit to desirable vertical tail size from a stability and control standpoint, but vertical tails that are too small lead to a variety of undesirable characteristics. For example, airplaneswith low weathervane stability require heavy coordinated rudderaileron inputs when beginning and stopping turns, especially at low airspeeds. When Walter Brewer, Professor Otto Koppen's former student, brought the Curtiss XSB2C-1 wind-tunnel model to the Wright BrothersWind Tunnel at MIT in 1939, Koppen said, "If they build more than one of those things, they're crazy," and further, "You don't need wind-tunnel balancesfor data, all you need isa record player under the tunnel saying, 'put on a bigger vertical tail!'"

The necessity of a powerful rudder for recovery from erect and inverted spins led to notched elevatorsto allow full rudder deflection in either direction. The much neater and lower drag solution of the P-51 Mustang, in which the rudder hinge line lies behind the elevator trailing edge, seems to have occurred independently to designers at Focke-Wulf and was rapidly adopted by other designers. Aerodynamic damping in pitch and yaw is proportional to the square of the tail arm. Since the damping of the Dutch roll oscillation is inherently poorer than the short-period pitch oscillation, it is better to have a longer vertical tail arm.

Before the constraints on vertical tail function were well understood, airplane manufacturers built vertical tails in distinctive shapes. L. Eugene Root, then at Douglas El Segundo, changed all that with a U.S. patent that describes straight-tapered tail surfaces with leading edgesand hinge linesall at a constant percentage chord.

## **6.2 Estimation from Drawings**

## **6.2.1** *Early Methods*

The elements of stability and control prediction from drawings started to be available as early as aerodynamic theory itself. That is, aside from elements such as propellers and jet intakes and exhausts, airplane configurations are combinations of lifting surfaces and bodies. However, it took some time before the lift and moment of lifting surfaces and bodies were codified into a form useful for preliminary stability and control design. Simple correlations of lift and moment with geometrical characteristics such as wing aspect and taper ratiosand the longitudinal distributionsof body volume were needed.

## **6.2.2** *Wing and Tail Methods*

For stability and control calculations at the design stage, the variations of lift coefficient with angle of attack, or lift curve slope, are needed for airplane wings and tail surfaces. Wing and tail lift curve slopes are to first-order functions of aspect ratio and sweepback angle, and to a lesser extent of Mach number, section trailing-edge angle, and taper ratio. The primary aspect ratio effect isgiven by Ludwig Prandtl'slifting line theory and can be found as charts of lift curve slope versus aspect ratio in early stability and control research reports. The sweepback effect was added by DeYoung and Harper (1948).

However, classical lifting line theory for wings and tails fails for large sweep angles and low aspect ratios, even at low Mach numbers. A 1925 theory of supersonic airfoils in two-dimensional flow due to Ackeret existed, and also in the 1920s Prandtl and Glauert showed how subsonic airfoil theory could be corrected for subsonic Mach number effects. Both the Ackeret theory and Prandtl-Glauert subsonic Mach number correction theory fail at Mach 1. R. T. Jones(1946) developed a very low aspect-ratio wing theory, valid for all Mach numbers, which applies to highly swept wings, that is, wings whose leading edges are well inside the Mach cone formed at the vertex.

### **6.2.3** *Bodies*

A fundamental source for the effectsof bodieson longitudinal and directional stability is the momentum or apparent mass analysis of Max M. Munk (1923). This models the flow around nonlifting bodies such as fuselages, nacelles, and external fuel tanks in terms of the growing or diminishing momentum imparted to segments of the air that the body passesthrough. Pitching and yawing momentsasfunctionsof angle of attack and sideslip are found by this method.

#### **6.2.4** *Wing–Body Interference*

The longitudinal, lateral, and directional stability of wingsand bodiesin combination are the isolated characteristics plus effects that reflect modification of the flow by interference. In the longitudinal case, upwash ahead of the wing and downwash behind the wing change the body local anglesof attack that enter into the Munk momentum theory calculations. Munk'sapparent masstheory for bodieswasextended by HansMulthopp (1941) to account for the nonconstant fuselage angle of attack due to the wing's flow field. Gilruth and White (1941) used strip theory for this modification.

Stability and control designers have known for some time that whether an airplane has a high or a low wing influences static directional and lateral stabilities. There was an organized study of this at NACA starting in 1939 as a part of a broader attack on the factors influencing directional and lateral stability. The wing position part of the study was completed in 1941 by House and Wallace.

Distortion of the wing's spanwise lift distribution and trailing vortex system due to sideslip has the following systematic effects:

> Low wing airplanes: Static lateral stability is reduced by about 5 degrees of equivalent wing dihedral ascompared with mid-wing airplanes. Thisrule of thumb haslasted to the present day. Static directional or weathervane stability is increased.

> High wing airplanes: The reverse of the low wing case. Dihedral effect is increased by about 5 degrees, weathervane stability is decreased.

**Cross-Flow Concept** The cross-flow concept aids in understanding aerodynamic forces for an airplane in sideslip. The total velocity vector VEL of an airplane in sideslip can be resolved into a component U along the X or longitudinal body axis and a component V along the Y or lateral body axis. The U component gives rise to a symmetric flow, while the V component gives rise to a hypothetical flow at right angles, along the Y body axis. The component flowsadd together to make up the total streamline pattern of the airplane in sideslip.

The V or cross-flow component is represented in Figure 6.2. This figure provides an explanation for the effectsof high and low wing positionson stability. The effectsare the result of the distortion of a wing's span load distribution in sideslip. Undistorted wing span load distributions feature sharp gradients of load with spanwise distance at both wing tips.

![Chapter 6 - Figure 1](../assets/chapter6/_page_4_Figure_1.jpeg)

**Figure 6.2** Cross-flow explanation of wing vertical position effects on directional stability and dihedral effect. Distortion of the wing span load in right sideslip creates a center vortex that gives destabilizing sidewash for a high wing and stabilizing sidewash for a low wing. The distorted span load gives increased dihedral effect for a high wing and decreased dihedral effect for a low wing.

Local shed vortex strength is proportional to this gradient, resulting in the familiar wing tip vortices. The flow of air from higher to lower pressure determines the sense of vortex rotation. Thuswing tip vorticesrotate to create downflow, or downwash, inboard of the wing tip.

The center vortices shown in Figure 6.2 are the result of the local span load distortion due to wing–fuselage interference in sideslip. Center vortex rotations for low and high wing arrangements in sideslip are seen to be consistent with the observed stability changes noted above.

## **6.2.5** *Downwash and Sidewash*

The flow behind wing–body combinations is deflected from the free-stream values, affecting the stabilizing contributions of the tail surfaces. Downwash is the downward deflection of the free stream behind a lifting surface, a momentum change consistent with the lift itself. Sidewash is a sideward deflection of the free stream, related to the side force on the wing–fuselage combination in side-slipping flow. Sidewash at the vertical tail is dominated by vortices that accompany the downwash when sideslip distorts the pattern.

Wing downwash charts for the symmetric flow (no sidewash) case suitable for preliminary design became available in 1939 from Silverstein and Katzoff. Later investigators broadened the design chartsto include the effectsof landing flap deflection, ground plane interference, wing sweep, and compressibility.

An interesting sidewash effect is the loss in directional stability experienced by receiver aircraft in close trail to tanker aircraft. Following reports of directional wandering of receiver aircraft, Bloy and Lea (1995) tested tanker–receiver model combinations in a low-speed wind tunnel. These results, together with vortex lattice modeling, confirm the loss in receiver directional stability. Rolled-up tanker wing tip vortices acting on the receiver vertical tail in a low position cause the problem.

#### **6.2.6** *Early Design Methods Matured – DATCOM, RAeS, JSASS Data Sheets*

New stability and control problems associated with geometries appropriate to transonic and supersonic speeds and their approximate theoretical or empirical consequences led to the creation of handbook data for their solution in a form suitable for the use of airplane designers. Handbooks have been produced by the USAF Wright Air Development Center, the British Royal Aeronautical Society (RAeS), the Japan Society for Aeronautical and Space Sciences (JSASS), and others. The USAF version, called DATCOM, for Data Compilation (Hoak, 1976), is supplemented by a computer version intended to reduce the manual labor in using the rather bulky hard copy version of the material.

The goal of all these compilations is to show the effects of all possible design factors on aircraft forcesand moments. Chartsand elaborate formulasare used, asin the example of Figure 6.3, from the DATCOM. RAeS data sheets have similar function and appearance, except for a wide use of ingenious carpet plots. Dr. H. H. B. M. Thomas played a key role in the development of the RAeS data sheets.

#### **6.2.7** *Computational Fluid Dynamics*

Computational fluid dynamic methodsapply the power of modern digital computers to the problem of estimating stability and control from drawings at the design stage. Finite-element methodsare one form of computational fluid dynamics. The great power of computational fluid dynamicsisitsability to deal with arbitrarily shaped airplanes. Even advanced handbook methods such as the DATCOM can fail to represent a truly unusual design.

Computational aerodynamicsare not exactly new, in that approximate methodsfor the calculation of aerodynamic loads on arbitrarily shaped wings in subsonic flow have been available for many years. However, before the advent of the digital computer the number of unknownsin the mathematical solutionsfor the flow had to be kept low. Aspointed out by Sven G. Hedman, one of the inventorsof the modern vortex lattice method, the number of unknownswaskept low in the predigital computer era by assumptionsfor the wing's chordwise and spanwise load distributions. That early work was done by Falkner (1943), who also coined the term *vortex lattice theory*.

Assumed load distributions are not needed for modern finite-element methods using the digital computer. The earliest applications of modern finite-element methods to the calculation of aerodynamic forcesand momentsappearsto have been made at the Boeing Company in about 1960. Thiswasthe discrete loading vortex lattice method, developed independently by Sven G. Hedman and P. E. Rubbert. The development of the vortex lattice method is a classic case of research people all over the world contributing steps to a remarkably useful result. For a detailed history, see De Young (1976).

## **6.2.7.1** *Vortex Lattice Methods*

When the vortex lattice method is applied to wings, the surface is arbitrarily divided in the chordwise and spanwise directions into panels or boxes. Each panel contains a horseshoe vortex. The vortex-induced flow field for each panel is derived by the Biot-Savart

$$\mathbf{c}\_{\mathbf{l}\_{\mathcal{B}}} = \mathbf{c}\_{\mathbf{l}} \left[ \left( \frac{\mathbf{c}\_{\mathbf{l}\_{\mathcal{B}}}}{\mathbf{c}\_{\mathbf{L}}} \right)\_{\mathbf{\hat{A}}\_{\mathbf{e}/\mathbf{L}}}, \mathbf{x}\_{\mathbf{M}\_{\mathbf{A}}} + \left( \frac{\mathbf{c}\_{\mathbf{l}\_{\mathcal{B}}}}{\mathbf{c}\_{\mathbf{L}}} \right)\_{\mathbf{A}} \right] + \mathbf{r} \left( \frac{\mathbf{c}\_{\mathbf{l}\_{\mathcal{B}}}}{\Gamma} \mathbf{x}\_{\mathbf{M}\_{\mathbf{I}}} \right) \\ \star \text{ } \boldsymbol{\tan} \, \boldsymbol{\Lambda}\_{\mathbf{e}/\mathbf{4}} \stackrel{\scriptstyle \Delta \mathbf{C}\_{\mathbf{l}\_{\mathcal{B}}}}{\boldsymbol{\theta} \, \tan \, \boldsymbol{\Lambda}\_{\mathbf{e}/\mathbf{4}}} \text{ (per degree)}$$

![Chapter 6 - Figure 1](../assets/chapter6/_page_6_Figure_4.jpeg)

**Figure 6.3** Example formula and chartsfrom the USAF DATCOM. Thiscoversonly a small part of the material for calculation of the derivative C1<sup>β</sup> for straight-tapered wings. RAeS data sheets have similar functions and appearance.

law. While this implies incompressible flow, the Prandtl-Glauert rule can extend the results to subcritical Mach numbers. The boundary condition of no flow across panels is fulfilled at just one control point per panel. Angle of attack and load distributions for the panels are found from a system of simultaneous linear equations that are easily solved on a digital computer. Distortions in data due to Reynolds' number mismatches, jet boundary corrections, and model attachment problems in real wind tunnels are replaced with the necessary approximationsof computational fluid dynamics.

When the panelslie in a flat plane and occupy constant percentage chord lineson an idealized straight-tapered wing at more or less arbitrary spanwise locations, and when each panel containsa line vortex acrossitslocal quarter chord point and trailing vorticesalong its side edges, whose collective vorticity provides tangential flow at every panel local threequarter–chord point, the bound vorticity in each panel can be found by desktop methods, as in the Weissinger method. However, when panels or a mesh cover a complete airplane configuration, automatic machine computation methods become necessary. Depending on the method used, the computer defines the vortex strength for each panel.

#### **6.2.7.2** *Generalized Panel Methods*

Following the pioneering vortex lattice work, computational fluid dynamicsprograms of increasing complexity have been developed, such as PAN AIR by Boeing, QUADPAN at Lockheed, Analytical Methods, Inc.'s, VSAERO, and MCAERO at McDonnell-Douglas. These approaches have included the Neumann problem in potential flow (Smith, 1962), inviscid Euler methods (Jameson, 1981), and full-blown Navier-Stokes equation solutions (Pulliam, 1989).

Vortex lattice, Euler, and Navier-Stokesmethodsare now used to generate airplane stability and control data at the preliminary design stage in much the same way that wind-tunnel models were used in earlier times. The computer defines and stores the three-dimensional panel geometry approximating the airframe shape, as in Figure 6.4. Aircraft lift curve slopes, static longitudinal and lateral stability, control effectiveness, and even rotary derivatives are well predicted for small angles of attack, sideslip, and control deflection.

## **6.3 Estimation from Wind-Tunnel Data**

Manufacturers of transport and military airplanes spend a great deal of money and engineering effort on wind-tunnel testing in developing new designs. These costs are rarely questioned anymore; one just budgets wind-tunnel testing at a generous level. Yet, how well can one expect wind-tunnel test results to match stability and control flight test results? This question was dealt with in an early NACA study (Kayten and Koven, 1945). Both engineers later led the stability and control branch in the U.S. Naval Air Systems Command.

Kayten and Koven compared wind-tunnel and flight test measurements for the Douglas A-26 Invader twin-engine attack airplane. The discrepancies were larger than one might have expected. Most of the discrepancies could be explained after the fact, but one is left with the uneasy feeling that wind-tunnel tests can give engineers a distinctly cloudy crystal ball. The factors that led to discrepancies in the case of the A-26 were

1. The geometric wing dihedral wasgreater in flight than in the wind tunnel due to upward bending under load. Thisproblem could be dealt with by giving tunnel models extra wing dihedral based on calculated bending deflections.

![Chapter 6 - Figure 1](../assets/chapter6/_page_8_Figure_1.jpeg)

**Figure 6.4** PAN AIR panel geometry for a computational fluid dynamic analysis of a complete airplane configuration. (From Tinico, Boeing Commercial Airplane Group, 1992)

- 2. Control surface contours in flight differed from the wind-tunnel model because of fabric distortion. This problem may have effectively vanished, since fabric-covered control surfaces are now rarely used.
- 3. There was premature inboard wing stalling in flight that was not present on the smooth, well-faired wind-tunnel model wing. This last problem is of the type that isdifficult to deal with in advance. However, the current approach might be to clean up the airplane's premature wing stalling by refairing or vortex generators, incidentally bringing about better agreement between the wind-tunnel and flight data.

In spite of discrepancies such as these, designers ignore unfavorable wind-tunnel results at their peril. For example, before it was flown, power model tests of the Martin 202 showed that itsone-piece wing would have negative effective dihedral in the power approach condition. The results were dismissed with the comment, "It's only a wind- tunnel test," but an expensive redesign was needed later.