# *Evolution of the Equations of Motion*

There isa reproduction in Chapter 1 of George H. Bryan'sequationsof airplane motion on moving axes, equations developed from the classical works of Newton, Euler, and Lagrange. This astonishingly modern set of differential equations dates from 1911. Yet, Bryan'sequationswere of no particular use to the airplane designersof hisday, assuming they even knew about them.

Thischapter tracesthe evolution of Bryan'sequationsfrom academic curiositiesto their present status as indispensable tools for the stability and control engineer. Airplane equations of motion (Figure 18.1) are used in dynamic stability analysis, in the design of stability augmenters (and automatic pilots), and as the heart of flight simulators.

#### **18.1 Euler and Hamilton**

One of the problemsfaced by Bryan in developing equationsof airplane motion was the choice of coordinates to represent airplane angular attitude. Bryan chose the system of successive finite rotations developed by the eighteenth-century Swiss mathematician Leonhard Euler, with a minor difference. In Bryan'swords:

> In the [Eulerian] system as specified in Routh's *Rigid Dynamics* and elsewhere, the axes are first rotated about the axisof z, then about the axisof y, then again about the axisof z. The objection to this specification is that if the system receives a small rotation about the axis of x, thiscannot be represented by *small* valuesof the angular coordinates.

Bryan chose instead to rotate by a yaw angle about the vertical axis, a pitch angle about the lateral axis, followed by a roll angle about the pitch axis– a sequence that hasbeen followed in the field ever since. However, Bryan'sorthogonal body axesfixed in the airplane are rotated by 90 degreesabout the X-axisascompared with modern practice. That is, the Y-axisisin the place of the modern Z-axis, while the Z-axisisthe negative of the modern Y-axis(Figure 18.2).

Bryan's Eulerian angles have served the stability and control community well in almost all cases. However, there were other choices that Bryan could have made that would have avoided a singularity inherent in Euler angles. The singularity shows up at pitch angles of plus or minus 90 degrees, the airplane pointing straight up or straight down. Then the equation for yaw angle rate becomesindeterminate.

The Euler angle singularity at 90 degrees is avoided by the use of either quaternions, invented by Sir W. R. Hamilton, or by direction cosines. The main disadvantage of quaternionsand direction cosinesasairplane attitude coordinatesistheir utter lack of intuitive feel. Flight dynamicstime historiescalculated with quaternionsor direction cosinesneed to be translated into Euler angles for intelligent use. Except for simulation of airplane or space-vehicle vertical launch or of fighter airplanes that might dwell at these attitudes, the Euler angle singularity at 90 degreesisnot a problem.

As the term implies, there are four quaternion coordinates; there are nine direction cosine coordinates. Since, as Euler pointed out, only three angular coordinates are required

**Figure 18.1** The 12 equations of airplane rigid-body motion, used extensively in flight simulation. All but three are in classical state-variable form, suitable for sequential application of computer integrating subroutines. Substituting the seventh into the eighth equation puts that one into state-variable form. A matrix inversion of the tenth and twelfth equationsputsthem into state-variable form.

to specify rigid-body attitudes, quaternion and direction cosine coordinates have some degree of redundancy. Thisredundancy isput to good use in modern digital computations to minimize roundoff errorsin an orthogonality check. Another advantage to quaternion as compared with Euler angle coordinatesisthe simple form of the quaternion rate equations, which are integrated during flight simulation. Euler angle rate equations differ from each other, are nonlinear, and contain trigonometric functions. On the other hand, quaternion rate equationsare all alike and are linear in the quaternion coordinates.

The nine direction cosine airplane attitude coordinates are identical to the elements of the 3-by-3 orthogonal matrix of transformation for the components of a vector between two

![Chapter 18 - Figure 1](../assets/chapter18/_page_2_Figure_1.jpeg)

**Figure 18.2** The Euler angle sequence in most common use as airplane attitude coordinates in flight dynamicsstudies. Thissequence wasdefined by B. Melvill Jonesin Durand's *Aerodynamic Theory*, in 1934. (From Abzug, DouglasRept. ES 17935, 1955)

coordinate systems. As in the quaternion case, all nine direction cosine rate equations have the advantage of being alike in form, and all are also linear. The direction cosine rate equationsare sometimescalled *Poisson's equations*. Airplane equationsof motion using quaternions are common; those using direction cosine attitude coordinates are rare.

The Euler parameter form of quaternionsusesdirection cosinesto define an axisof rotation with respect to axes fixed in inertial space. A rotation of airplane body axes about that axisbringsbody axesto their proper attitude at any instant (Figure 18.3). Thisgoes back to one of Euler's theorems, which states that a body can be brought to an arbitrary attitude by a single rotation about *some* axis. There is no intuitive feel for the actual attitude corresponding to a set of Euler parameters because the four parameters are themselves trigonometric functionsof the direction cosinesand the rotation angle about the axis.

The first published report bringing quaternions to the attention of airplane flight simulation engineerswasby A. C. Robinson (1957). Robinson'scontribution wasfollowed in 1960 by D. T. Greenwood, who showed the advantages of quaternions in error checking numerical computations during a simulation. A detailed historical survey of all three attitude coordinate systems is given by Phillips, Hailey, and Gebert (2001). The flight simulation

$$\mathbf{e}\_1 = \cos \mu \mathbf{\hat{z}}$$
$$\mathbf{e}\_3 = \cos \beta \text{ sin} \mu/2$$

![Chapter 18 - Figure 1](../assets/chapter18/_page_3_Figure_8.jpeg)

$$\begin{array}{lcl}\Theta & = \sin^{-1}[2(\mathbf{e}\_{\mathrm{i}}\mathbf{e}\_{\mathrm{s}} \cdot \mathbf{e}\_{\mathrm{2}}\mathbf{e}\_{\mathrm{4}})] \\\\ \Phi & = \tan^{-1}[2(\mathbf{e}\_{\mathrm{i}}\mathbf{e}\_{\mathrm{2}} + \mathbf{e}\_{\mathrm{4}}\mathbf{e}\_{\mathrm{1}})/(\mathbf{e}\_{\mathrm{4}}\mathbf{z}^{\mathrm{2}} \cdot \mathbf{e}\_{\mathrm{s}}\mathbf{z}^{\mathrm{2}} + \mathbf{e}\_{\mathrm{2}}\mathbf{z}^{\mathrm{2}} + \mathbf{e}\_{\mathrm{1}}\mathbf{z})] \\\\ \Psi & = \tan^{-1}[2(\mathbf{e}\_{\mathrm{4}}\mathbf{e}\_{\mathrm{i}} + \mathbf{e}\_{\mathrm{2}}\mathbf{e}\_{\mathrm{1}})/(\mathbf{e}\_{\mathrm{4}}\mathbf{z}^{\mathrm{2}} \cdot \mathbf{e}\_{\mathrm{2}}\mathbf{z}^{\mathrm{2}} + \mathbf{e}\_{\mathrm{1}}\mathbf{z})] \end{array}$$

**Figure 18.3** The Euler parameter form of quaternions used in some flight simulations to calculate airplane attitude. The upper group of equationsdefinesthe Euler parametersin termsof an axisof rotation of XYZ to a new attitude. {*x*}body are vector componentson the rotated axes; {*x*}earth are the same components on the original axes. Transformations between Euler parameters and Euler angles are given in the lower two sets of equations.

![Chapter 18 - Figure 1](../assets/chapter18/_page_3_Figure_16.jpeg)

community appearsto be divided on the choice between Euler anglesand quaternions. In some cases, both are used in different flight simulators within a single organization. However, it is interesting that so many modern digital computations of airplane stability and control continue to use Euler angle coordinates in the 1911 Bryan manner.

## **18.2 Linearization**

In their basic form, the equations of airplane motion are a set of nine simultaneous nonlinear differential equations. One of the most far-reaching steps taken by Bryan was the development of a perturbation, linearized, form of these equations. The perturbation motion of a simple mechanical object, such as a pendulum, about a state of rest is a familiar concept. In his *M´ecanique Analytique* of 1788, J. L. Lagrange developed the theory of small perturbation motions of systems having many degrees of freedom about a position of stable equilibrium. Bryan extended Lagrange's work by replacing the position of stable equilibrium by a steady equilibrium motion.

The utility of Bryan'slinearization arisesfrom the nature of airplane perturbed motions. Under normal operating conditions, such as personal-airplane and airliner climbs, cruises, and landing approaches, airplanes are among the most linear dynamic systems known. Aerodynamic force and moment are quite closely proportional to airplane perturbed motions, without any equivalent to coulomb friction. Small-perturbation or linearized equations are perfectly suitable to describe the motions experienced by the crew and passengers, and for the design of stability augmenters and automatic pilots.

Bryan analyzed small perturbations about steady, symmetric, rectilinear flight, either level, climbing, or diving. Most of the subsequent literature on airplane dynamics is based on the same model. Equations of perturbed airplane motion about steady turning and steady sideslipping flight came soon after Bryan, in an important 1914 report by Leonard Bairstow. A further extension to general curvilinear flight was made using earth-referred coordinates (Frazer, Duncan, and Collar, 1938). Still later investigators (Abzug, 1954; Billion, 1956) used the more useful body-fixed coordinates. Then, in a series of NASA papers dating from 1981 to 1983, Robert T. N. Chen applied linearization to the case of perturbations from uncoordinated turns. Chen'simmediate goal wasto represent perturbation motions of single-rotor helicopters in low-airspeed, steep turns, in which appreciable amounts of sideslip are quite normal.

The 1914 linearization work by Bairstow suffered the fate of theory that was too far ahead of its time. The later investigators mentioned above seemed to have been unaware that Bairstow had already extended the original Bryan equations.

Bryan'slinearization of the equationsof airplane motion reducesthem to two setsof three simultaneous linear differential equations, each set of fourth order. The linearized equations shown in Figure 18.4 illustrate three typical features of these equations. Differentiation is indicated by the Laplace variable *s*, operating on the small-perturbation quantities such as *u*, *w*, θ, and β. Aerodynamic variations with small-perturbation quantities, called stability derivatives, are in the "dimensional" form, suitable for closed-loop system studies and for simulation.

Finally, the derivativesare the primed form such as *Lp* rather than *Lp* for the rolling moment due to rolling velocity. Primed derivativescombine inertial termswith aerodynamic terms, simplifying the lateral set and putting these equations into state-variable form (Sec. 11).

The fact that the linearized equationsof motion separate into two independent setsisof enormoussignificance. Engineerscan treat airplane dynamicsastwo individual problems:

**Figure 18.4** Dimensional forms of the small-perturbation equations of airplane motion, suitable for closed-loop system studies. The longitudinal set is above, the lateral set below. Output equations, for calculation of some sensor readings, are listed below the matrix sets. (From Teper, Systems Technology, Inc. Rept. 176–1, 1969)

longitudinal stability and control, arising from the symmetric equation set, and lateral stability and control, arising from the asymmetric set. However, separation into independent longitudinal and lateral setsfailsfor perturbationsfrom curvilinear or sideslipping flight. Coupled lateral-longitudinal equations of up to eighth order result. Bairstow (1920) treated perturbationsfrom circling flight.

# **18.3 Early Numerical Work**

Useful solutionsto Bryan'sequationsof airplane motion for scientific or engineering uses are either roots or eigenvalues or actual time histories, which give airplane responses to specific control or disturbance inputs. Either type of solution was essentially out of the question with the means available in 1911. However, by 1920 Bairstow had found useful approximationsthat served asstarting pointsfor developing eigenvaluesfrom the Bryan equations.

When, later on, research engineers in both the United States and in Britain generated time history solutions to the linearized Bryan equations, it was only with great labor. Early step-by-step numerical solutions were published for the S.E.-5 airplane of World War I fame by F. Workman in 1924. A year later, B. Melvill Jonesand A. Trevelyan (1925) published step-by-step solutions for the lateral or asymmetrical motions.

As an advance over step-by-step methods, B. Melvill Jones (1934) applied the formal mathematical theory of differential equationsto the linearized Bryan equations, producing a marvelously complete set of time histories for the B.F.2b Bristol Fighter at an altitude of 6,000 feet (Figure 18.5). A generation of pre–electronic-computer engineers struggled through those formal solutions. The complementary function is found first. In addition to using a considerable amount of algebra, one has to find the real and complex rootsof a fourth-degree polynomial. The complementary function givesthe time histories of the variablesof motion under no applied forcesand moments, but with arbitrary initial conditions.

The last step in the formal solution is finding a particular integral of the equations. Thisaddsto the complementary function the effectsof constant applied moments, such asare produced by deflectionsof the airplane'scontrol surfaces. In Jones' own words, "The numerical computations involved . . . are heavy, they involve amongst other things, the solution of four simultaneous equations with four variables." It is little wonder that numerical time history calculations languished for years, until electronic analog computers were commercially available, about the year 1950.

#### **18.4 Glauert's and Later Nondimensional Forms**

Hermann Glauert'scontribution to the evolution of the equationsof airplane motion was to introduce a dimensionless system based on the time unit τ = µ*1*/*V*. In the expression for τ , µ isthe airplane relative density *m*/ρ*S1*, and ρ isthe air density. *1* and *S* are the airplane's characteristic length and area, respectively. Typically *1* isthe wing span and *S* the wing area. *V* is the airspeed. The relative density µ is the ratio of airplane mass to the mass of air contained in a volume *S* × *1*, determined by airplane size. Under Glauert's system, time solutionscome out in unitsof τ seconds.

When the Glauert processiscarried out, the numerical valuesof all symbolsthat appear in the equations(except for µ) depend only on the airplane's shape, mass distribution, attitude, and angles of attack and sideslip. Airplane size, velocity, mass, and the air density, or altitude of flight, are all represented by the single parameter µ.

Glauert defined new boldfaced dimensionless symbols such as **t**, **w**, **q** for time, vertical velocity, and pitching velocity, and **k** with an appropriate subscript for moment of inertia divided by *1*<sup>2</sup> times *m*. The stability derivatives are likewise nondimensionalized. For example, **x***<sup>w</sup>* stands for (*d*X/*dw*)/ρ*VS*. AsB. Melvill Jones(1934) says:

When it is desired to convert the solutions so as to apply to a specified flight of a specified aeroplane in terms of specified units, it is merely necessary to multiply **u , v, w**, by **V**/µ; **p, q, r**, by **V**/µ*1*, and **t** by τ (or *m*/ρ**V***S* ); where µ, **V**, *1*, *S* relate to the specified flight and are expressed in terms of the specified units.

If this is confusing to the reader, it was also confusing to the generation of stability and control engineerswho practiced their art before electronic analog and then digital computers transformed the picture. Airplane time history calculations are now easy to make, so that there is no longer a premium on allowing a single dimensionless computation to represent many altitude, velocity (but not Mach number), size, and mass cases.

![Chapter 18 - Figure 1](../assets/chapter18/_page_7_Figure_1.jpeg)

**Figure 18.5** Examples of equation of motion solutions for the Bristol F.2b (Bristol Fighter) produced in the 1930sfor B. Melvill Jones' section in Durand's *Aerodynamic Theory*. The pitch attitude and normal acceleration solutions are for initial airspeed and vertical velocity perturbations and step elevator angles, at different equilibrium angles.

Aerodynamic data are generated in dimensionless form as the computed output of windtunnel tests and are so presented to the engineers that use equations of airplane motion. However, the special time unit τ has all but disappeared from the scene. Airplane motions are calculated in terms of actual, rather than dimensionless, velocity units, except for the angles of attack and sideslip. In Glauert's day dimensionless aerodynamic coefficients in Britain were based on ρ*V*2, not (ρ/2)*V*2. Thus, Glauert's dimensionless stability derivatives were half as big as NACA dimensionless stability derivatives, except for the pitching moment rate derivatives *mw* and *mq* , based on the time to fly a chord, not a half-chord.

It is hard to avoid the impression that Glauert's ingenious nondimensional form of the equations of airplane motion put the dynamic stability and control field on a side track that ultimately led nowhere. Thisparticular contribution of the brilliant Hermann Glauert was undone by the digital computer.

Special notation for the equations of airplane motion actually started before Glauert (see Bryant and Gates, 1937). Notation for the equationsof airplane motion remainsan interest in Britain, the country where it all began. As part of its "Engineering Sciences Data" series, the Royal Aeronautical Society issued in 1967 a review of airplane dynamics notation and a recommended new set of standards. This work built on an impressive five-part RAE Technical Report (Hopkin, 1966). Hopkin'spoint of view is

Notation is an extension of language, and a Tower of Babel should not be allowed to grow.

By the time of Hopkin'swork, the growth in applicationsof the equationsof airplane motion had produced a great number of possible notational methods. In order to accommodate them all without ambiguity, Hopkin was obliged to use unusual symbols, such as little half-moons over symbols. These seem not to have caught on, at least in the United States. Authorsapparently are content to define symbolsthat are clear enough in the context of their work.

A dimensional form of the stability derivatives has become popular especially for linearized analysis, in which the derivatives are divided by either airplane mass or a moment of inertia function. This form provides airplane state vectors that are physically measurable, such as velocities and angular velocities. In this system the derivative **Z***<sup>u</sup>* stands for (∂**Z**/∂*u*)/*m*, for example. Thisparticular form of the stability derivativesisfound in the reportsof the influential SystemsTechnology, Inc., group.

# **18.5 Rotary Derivatives**

Rotary stability derivativesare the variationsin force and moment coefficients with airplane angular velocity. Angular velocity is almost always made dimensionless in rotary derivativesby multiplication by a factor *1*/(2*V* ), where *1* stands for either the wing chord *c* or span *b* and *V* isthe velocity. A typical rotary derivative isthe pitch damping derivative *Cmq* , defined as ∂*Cm*/(∂*qc*/2*V* ).

Rotary derivativeswere neglected in the original Bryan andWilliamsequationsof motion (Bryan and Williams, 1903), since there was then no way to measure them. However, Bryan was later able to describe two techniques for rotary derivative measurement: putting a model on a whirling table or at the end of a whirling arm, and oscillating a model in an otherwise conventional wind tunnel (Bryan, 1911).

The oscillation technique survived right up to modern times. It is used in supersonic as well as in low-speed wind tunnels. An ingenious forced oscillation technique for measuring rotary derivativesusesfeedback control to stabilize the amplitude and frequency of a forced oscillation regardlessof the model'slevel of stable or unstable derivatives(Beam, 1956).

An additional feature of Beam's forced oscillation method is the separation of pitch and yaw damping derivatives from the cross-rotary derivatives, such as the rolling moment due to yawing, by oscillating the model around different axes. In- and out-of-phase torque measurements are solved simultaneously for the answers. The drawback in Beam's work is that the damping derivativessuch as *Cmq* and *Cnr* are inseparable from angle of attack and side-slip rate derivatives, such as *Cm*α˙ and *Cn*β˙. This separation is possible in specialized forced-motion wind-tunnel tests.

One of the few wind tunnelsthat produced pure damping derivativeswasthe NACA Langley Stability Wind Tunnel. The past tense is used because the Stability Wind Tunnel was dismantled some years ago and shipped to the Virginia Polytechnic Institute. The Stability Wind Tunnel had curved test sectionsin which the forcesand momentson an ordinary model were the result of rotary flows. This yielded the rotary derivatives uncombined with attitude rate derivatives. The same effect was produced with curved airship models tested in ordinary wind tunnelsback in the 1920s.

The Stability Wind Tunnel also used radial turning vanes ahead of the test section to produce rolling flow. Flow angularity with respect to the wind-tunnel centerline was a linear function of distance from the centerline to the tunnel walls. The aerodynamic forces on a model held rigidly at the tunnel center would be identical to those of a rolling model in an ordinary wind tunnel, except for some transverse boundary layer motion caused by radial pressure gradient. The DVL in Germany experimented with rolling flow in wind tunnels in the 1930s.

The whirling arm asa device for measuring rotary derivativeshad a rebirth of sortsat the Cranfield College of Aeronauticsin the early 1960s(Mulkensand Ormerod, 1993). The motivation is support of a Royal Aircraft Establishment flight research program called HIRM, for High-Incidence Research Model. Carbon-fiber–reinforced plastic, foam, and fiberglass models are whirled on an 8.3-meter arm inside a toroidal test channel. Moving the modelsat constant angle of attack along circular pathsprovidespure rotary derivative data, equivalent to that gotten from curved flow wind tunnels.

#### **18.6 Stability Boundaries**

Until the advent of electronic analog and digital computers, numerical solutions of the equations of airplane motion were essentially limited to finding stability boundaries, the combinationsof airplane stability derivativesand other parametersthat divide stability from instability. Stability boundariesare found by Routh'sCriterion, developed by the Briton E. J. Routh in the early 1900s.

Airplane stability boundaries were first calculated in Britain (Bryant, Jones, and Pawsey, 1932). This was in a study of dynamic stability beyond the stall. Bryant and his co-authors found stability derivativesfor a number of airplanesup to an angle of attack of 40 degrees. With these data, they produced stability boundaries as functions of static directional and lateral stability derivatives, both nondimensionalized by Glauert's airplane relative density parameter µ.

There wasan earlier British paper by S. B. Gatesthat presented contoursof constant damping ratio and natural frequency for the longitudinal phugoid, asfunctionsof tail volume and center-of-gravity position (Gates, 1927). While not strictly a stability boundary analysis, the Gateswork certainly laid the groundwork for Bryant'sboundaries.

Two NACA reportsby CharlesH. Zimmerman (1935 and 1937) carried on Gates' and Bryant'spioneering stability boundary work. Zimmerman'sambitiousgoal wasto produce chartsfor the rapid estimation of the dynamicsof *any* airplane. The Zimmerman reports have chartsfor both longitudinal and lateral motions, 40 of the former and 22 of the latter (Figure 18.6). Asin Bryant'swork, the resultsare normalized using Glauert'sairplane density parameter µ. The Zimmerman chartsinclude period and damping estimatesfor the phugoid and Dutch roll motions.

# **18.7 Wind, Body, Stability, and Principal Axes**

One of the most distressing experiences for beginning stability and control engineersisto be faced with at least four alternate setsof reference axesfor the equations of airplane motion. The original Bryan set, called body axes, is perhaps the most easily

![Chapter 18 - Figure 1](../assets/chapter18/_page_10_Figure_1.jpeg)

**Figure 18.6** Representative lateral-directional stability boundaries. Spiral and directional divergence boundariesare given, along with approximationsfor Dutch Roll period and damping. The airplane relative density µ is used in the chart coordinates. (From Zimmerman, NACA Rept. 589, 1937)

grasped. Orthogonal reference axesare fixed in the airframe asif they were painted on, remaining in place through all subsequent motions. To be fair, even body axes can migrate with respect to the airframe, since the most common form has its origin at the airplane's center of gravity, which shifts about with different loadings.

Body axeshave the practical virtue that the variablesof motion that are calculated, such as the linear and angular velocities, are easily related to the readings of flight instruments, which are, after all, also fixed to the body. However, in the early days of stability and control analysis, there were advantages to wind axes (Zimmerman, 1935).

In wind axes, the forward or X-axis points into the wind during the entire motion, rotating about the center of gravity with respect to the airframe. The independence of translatory and rotational motionsallowsthisto happen without affecting the calculation of pitching motions. An advantage of wind axesisthat the X and Z forcesare the exact negativesof the familiar drag and lift forces presented in wind-tunnel test reports and used in airplane performance calculations.

Stability axescame into the picture in the 1940s, asa device to simplify calculation of small-perturbation airplane motions. Stability axes are a special set of body axes. The X stability axispointsinto the relative wind in the equilibrium flight that precedesthe disturbed motion, but remainsfixed in the body during the calculated motionsaround equilibrium. All that isaccomplished by stability axesisthe elimination of a few termsin the equations that include initial angle of attack. With the advent of powerful new digital computers stability axes have become mostly a curiosity, except for the fact that the primed derivatives mentioned in Sec. 2 have their basis in stability axes. Duane McRuer notes that

Primed derivatives based on stability axes often have a remarkably simple connection with the basic motions of the aircraft. . . . [For example] the square of the Dutch roll undamped natural frequency isusually given to a high degree of accuracy by *N* <sup>β</sup> ....stability axesare appropriate for determining the characteristic modes [of motion] and their predominant constituents.

To complicate things, the term *stability axes* sometimeshasquite another meaning than that of a special set of body axes for flight dynamics studies. Wind-tunnel data are quite often produced in what are called *stability axes*, but for clarity should be named *wind-tunnel stability axes*. The Z-axisisin the plane of symmetry and normal to the relative wind; the X-axisisin the plane of symmetry and isnormal to the Z-axis; the Y-axisisnormal to both X- and Z-axes.

Principal axes are another curiosity in present-day practice, since they are used only to eliminate the product of inertia termsin the equationsof motion. Aswith stability axes, principal axes have been obsoleted by powerful digital computers. A few added terms in the equationsseem to add nothing to computing time.

The hybrid case in which wind axes are used for the three force equations and body axes for the three moment equations can be found in some simulations. The first hybrid application the authorsare aware of wasmade by Robert W. Bratt at the DouglasAircraft Company's El Segundo Division, about 1955, in connection with inertial coupling studies. A more recent example of hybrid axesisNASA'sSIM2, which actually usesthree setsof axes, wind, wind-tunnel stability, and body (Figure 18.7). SIM2 was first put to use at the NASA Dryden Flight Research Center for real-time digital simulation of the McDonnell Douglas F-15. The aerodynamic data base was filled in to an angle of attack of 90 degrees, to allow simulation of stalls and spins. Later SIM2 applications were to the space shuttle Orbiter and to the Northrop B-2 stealth bomber.

With three axes systems carried along simultaneously in the solution, the angular relationships among the SIM2 axes sets must also be continuously computed. The fundamental force vector equation on moving axes used in SIM2 uses the vector cross-product of angular velocity of wind axesand the velocity vector. A key vector equation solvesfor the angular velocity of wind axesasthe angular velocity of body axesminustwo terms, the angular velocity of wind-tunnel stability axes with respect to wind axes and the angular velocity of body axes with respect to wind-tunnel stability axes.

Wind axes differ from wind-tunnel stability axes only by a positive sideslip angle rotation about the Z stability axis, so that the second of the three terms in the vector equation for wind axes angular velocity has only one nonzero element, the sideslip angle rate. Likewise, wind-tunnel stability axesare derived from body axesby a single angle of attack rotation

$$\begin{aligned} V &= X\_{\mathbb{W}} / m \\\\ \dot{\beta} &= (Y\_{\mathbb{W}} / \text{mV}) - R\_s \\\\ \dot{\alpha} &= Q - P\_s \tan \beta + Z\_{\mathbb{W}} / (\text{mV} \cos \beta) \end{aligned}$$

where

*X*<sup>w</sup> *Y*<sup>w</sup> *Z*<sup>w</sup> = cosβ sinβ 0 −sinβ cosβ 0 0 01 cosα 0 sin α 010 −sinα 0 cos α *X Y Z* 

and

$$\begin{array}{c} P\_s \\ \mathcal{Q}\_s \\ R\_s \end{array} = \begin{bmatrix} \cos\alpha & 0 & \sin\alpha \\ 0 & 1 & 0 \\ -\sin\alpha & 0 & \cos\alpha \end{bmatrix} \begin{bmatrix} P \\ \mathcal{Q} \\ R \end{bmatrix} $$

Note on symbols: Subscript w refers to wind axes, subscript s refers to (wind tunnel) stability axes. Unsubscripted symbols refer to body axes.

**Figure 18.7** One form of the force equations of motion for hybrid axes, in which wind axes are used for the force equations and body axes are used for the moment equations. This particularly compact form is used in the NASA-Northrop SIM2 digital simulation for the space shuttle Orbiter and the B-2 bomber.

along the negative Y-body axis. The required vector transformations are made in component form, always taking care to add components in the same axis systems.

The sideslip and angle of attack variables that define the difference among the three axis sets in SIM2 have one of the two possible definitions. The SIM2 convention happens to agree with the most common definition, in which wind axesare derived from body axesby an initial negative angle of attack −α rotation followed by a positive sideslip angle rotation β (Figure 18.8). The reverse convention is rare but not unknown.

Extended airplane axes sets that allow for flight at extreme speeds and altitudes, taking into account the earth'sactual shape, are treated in Sec. 15.

# **18.8 Laplace Transforms, Frequency Response, and Root Locus**

One of the minor mysteriesin the evolution of the equationsof airplane motion iswhy it wasnot until 1950 that the Laplace transformation appeared in the open literature asa solution method for the airplane equationsof motion. Thiswasin an NACA Technical Note by Dr. G. A. Mokrzycki (1950), who later anglicized hisname to G. A. Andrew. Laplace transforms were common among servomechanism engineers and in a few aeronautical officesfor at least ten yearsbefore that. Laplace transformsprovide a much simpler, more organized method for finding time history solutions than the classical operator methodsdescribed by B. Melvill Jones(1934) and Robert T. Jones(1936). Laplace transforms also provide a formal basis for airplane transfer functions, frequency responses, time vector analysis, and root loci, all used in the synthesis of stability augmentation systems, asdescribed in Chapter 20, "Stability Augmentation."

![Chapter 18 - Figure 1](../assets/chapter18/_page_13_Figure_1.jpeg)

**Figure 18.8** Usual angle-of-attack α and sideslip angle β convention, used in the NASA SIM2 flight simulation. X, Y, and Z are body axes. (From Abzug, Northrop paper, 1983)

# **18.9 The Modes of Airplane Motion**

Small-perturbation airplane motions are characterized by modes, just as the disturbed motions of two spring-coupled masses are a composite of a high-frequency mode of motion in which the masses move toward and away from each other, and a low-frequency mode in which the masses move in the same direction. The five classical modes of airplane motion are found asfactorsof the airplane'slongitudinal and lateral characteristic equations (Jones, 1934).

The characteristic equations are of fourth or higher degree, so that factors must be found by successive approximations, rather than in closed form. The factors are either real or they occur in pairs, in conjugate complex form. The real factors are characterized by times to double or halve amplitude following a disturbance or by the inverse of the factor, the time constant. The complex factors are usually characterized by their periods or frequencies (damped or undamped) and by their dimensionless damping ratios. The five classical modes are

- **Phugoid**, a low-frequency motion involving large pitch attitude and height changes at essentially constant angle of attack. Damping is low, especially for aerodynamically clean airplanes.
- **Longitudinal short period**, a rapid, normally heavily damped motion at essentially constant airspeed. Damping is provided by wing lift in plunging, as well as horizontal tail lift in rotation. Rapid pitch maneuversoccur in thismode.
- **Dutch roll**, a rolling, yawing, and sideslipping motion of generally low damping, especially at high altitudes.
- **Roll**, essentially a pure rolling motion about the airplane's longitudinal axis, heavily damped. The primary response to lateral controlsisin thismode.
- **Spiral**, a very slow divergence or convergence involving large heading changes, moderate bank angles, and near-zero sideslip.

Additional or combined modes appear in special circumstances, such as the supersonic height mode, discussed in Chapter 11. Notable combined modes are

- **Coupled roll-spiral or lateral phugoid**, the conversion of two simple, aperiodic modesinto one oscillatory mode. Thismode occurson airplaneswith high effective dihedral and low roll damping (Ashkenas, 1958; Newell, 1965). It has been observed on some V/STOL and high-speed airplanes.
- **Lateral divergence**, a degeneration of the Dutch roll mode into two aperiodic modes, one divergent.
- **Longitudinal divergence**, a degeneration of the phugoid or short-period modes into two aperiodic modes, one divergent. For the phugoid case, the divergent mode is called speed instability or tuck; for the short-period case the divergent mode iscalled pitchup.

Kinematically constrained modes of motion are those in which some flight variable such as altitude or bank angle is suppressed entirely by theoretical control surface or thrust closed loops, representing pilot control actions. The object is to get approximate stability criteria for flight conditionswhere the pilot isactively controlling a variable. Two such modesare

- **Constrained airspeed mode**, in which altitude ismaintained by some control moment, such aswould be produced by the elevator. Thisproducesa mathematical demonstration of speed stability (Neumark, 1957). The constraint results in a first-order differential equation in perturbation airspeed. There is an unstable real root for flight on the back side of the lift–drag polar, corresponding to lift coefficients above that for minimum drag. Section 2 of Chapter 12 discusses the implications of speed stability for naval aircraft.
- **Constrained yaw mode**, in which zero bank angle ismaintained by the ailerons (Pinsker, 1967). This constraint results in a first-order differential equation in perturbation yawing velocity. Pinsker demonstrated an aperiodic divergence at anglesof attack greater than 18 degreesfor an airplane with a low-aspect-ratio wing. This is similar to the nose slice experienced by some modern fighters. Stability of thisaperiodic mode isgoverned by the LCDP parameter (Chapter 9, Sec. 15) *Nv* − (*N*δ*<sup>a</sup>*/*L*δ*<sup>a</sup>*) *Lv* , where *Nv* and *Lv* are the yawing and rolling moments due to sideslip and *N*δ*<sup>a</sup>* and *L*δ*<sup>a</sup>* are the yawing and rolling moments due to aileron deflection.

The useful concept of airplane modes of motion has been extended to rotary-wing aircraft. In forward flight, their modes of motion are similar to those of fixed-wing aircraft. However, many of the usual stability derivatives disappear in hovering flight, giving quite different resultsfor the modesof motion in hover.

By adding apparent mass effects to the stability derivatives, one can obtain modes of motion for lighter-than-air vehicles. Cook (2000) used earlier models by Lipscombe, Gomes, and Crawford and recent wind-tunnel data to derive modesof motion for a modern nonrigid airship.

### **18.9.1** *Literal Approximations to the Modes*

A literal approximation to a mode of airplane motion isdefined asan approximate factor that is a combination of stability derivatives and flight parameters such as velocity or air density. This approximation is quite distinct from the factors that are obtained from the airplane's fourth- or higher degree characteristic equations, factors that are necessarily in numerical form. Literal approximationsto the modeshave a long history, starting with Lanchester in 1908. A feedback systems analysis approach to developing and validating approximate modeswasdeveloped by Ashkenasand McRuer (1958).

A well-known and usually quite accurate literal approximation to the roll mode is for the roll mode time constant *TR*. The roll mode time constant is the time required for rolling velocity to rise to 63 percent of its steady value following an abrupt aileron displacement. The approximation is *TR* = −<sup>1</sup> /*L*p. The symbol *<sup>L</sup>*<sup>p</sup> <sup>=</sup> *<sup>C</sup>*lp*q Sb*<sup>2</sup>/(2 *V Ix* ), where

- *Clp* = dimensionless roll damping derivative, a function of wing planform parameterssuch asaspect ratio and sweep angle;
- *<sup>q</sup>* <sup>=</sup> flight dynamic pressure, (ρ/2)*<sup>V</sup>* 2;
- *S* = wing area;
- *b* = wing span;
- *V* = flight velocity;
- ρ = air density;
- *Ix* = roll moment of inertia.

Note that all of the individual parametersin the roll mode approximation would normally be known to an airplane designer. A large literature has been produced on literal approximations to the modes. McRuer (1973) lists four reasons for this interest, as follows:

- 1. Developing the insight required for the determination of airframe/automaticcontrol combinations that offer possible improvements on overall system complexity.
- 2. Assessing the effects of configuration changes on aircraft response and on airframe/autopilot/pilot system characteristics.
- 3. Showing the detailed effectsof particular stability derivatives(and their estimated accuracies) on the poles and zeros and hence on aircraft and airframe/autopilot/pilot characteristics.
- 4. Obtaining stability derivatives from flight test data.

To this list one might add that mode approximations provide a reasonableness check on complete solutions generated within massive digital-computer programs, assuring that no input errorshave been made. Literal approximationsto the modesare obtainable only if the equations of motion themselves are simplified in some way, or if the factorization itself is approximated.

Mode approximationsare useful in the waysMcRuer listsaslong asthe approximations are simple ones, easy to grasp. One can improve the approximations, bringing the numerical valuescloser to the actual factorsof the characteristic equation. Thiscan provide additional insight into aircraft flight mechanics. However, if the literal expressions are lengthy, their utility suffers. The improvement to the classical Lanchester result for the phugoid mode period made by Regan (1993) and others(see Chapter 11, Sec. 13), which addsonly one simple term but greatly improves accuracy at high airspeeds, is an example of a useful improved approximation, in the context of McRuer'scomments.

On the other hand, the improved modal approximationsof Kamesh (1999) and Phillips (2000), while demonstrating considerable mathematical skills and adding to our understanding of flight dynamics, are probably too complex for the applications mentioned by McRuer.

#### **18.10 Time Vector Analysis**

The time vector analysismethod providesan excellent insight into the modesof airplane motion. The method came about asan incidental result of debugging one of the world's first electronic analog computers, built to represent generalized airplane longitudinal dynamics. Thiscomputer'sinventor wasDr. Robert K. Mueller; hisdevice, now in the MIT Museum, was built to support his 1936 MIT ScD thesis.

The fundamental concept of time vector analysis is that for any oscillatory transient generated by a linear system having a certain undamped natural frequency and damping ratio:

- 1. the amplitude of the transient derivative is the transient amplitude multiplied by the undamped natural frequency, and
- 2. the phase of the transient derivative is the phase of the transient advanced by 90 degreesplusthe angle whose sine isthe damping ratio.

With this concept, one can construct time vector polygons representing each term in any system equation corresponding to a particular modal solution of the characteristic equation. The time vector polygonsshow which termsare dominant and how the amplitude and phase relations among the variables arise (Figure 18.9). In Mueller's thesis example, the time vector polygonsgive insight into the wind axisequationsof longitudinal motion and suggest correction of the phugoid mode instability with pitch attitude feedback. At the urging of his then-supervisor at the Glenn L. Martin Company, James S. McDonnell, he presented a paper on the topic at a meeting of the Institute of Aeronautical Sciences (Mueller, 1937).

In Germany, Dr. Karl-H. Doetsch used the time vector method to study lightly damped airplane–autopilot combinations. Working at the Royal Aircraft Establishment (RAE) after World War II, K-H. Doetsch and W. J. G. Pinsker applied time vector analysis methods to the Dutch roll problemsof jet airplanes.

There wasan early application of the time vector analysismethod by Leonard Sternfield of the NACA Langley Laboratory to the Dutch roll oscillation. Around 1951 he built two bridge-table–size mechanical analogsof the roll and yaw time vector polygonsto predict the Dutch roll characteristics of new airplanes. Around the same time E. E. Larrabee made what he thought was the first use of time vector analysis to extract stability derivatives from flight time history measurements, although Doetsch had done much the same in England.

# **18.11 Vector, Dyadic, Matrix, and Tensor Forms**

Bryan used quite conventional cartesian coordinates in the derivation of the equations of airplane motion on moving axes, in 1911. Cartesian coordinates were used as well by subsequent investigators, such as B. Melvill Jones (1934), Charles Zimmerman (1937), and Courtland Perkins(1949). The first author who applied vector methodsto the derivation of these equationsappearsto have been LouisM. Milne-Thomson, in hisbook *Theoretical Aerodynamics* (1958).

The most notable thing about the Milne-Thomson vector derivation is the way in which a fundamental moving axisrate equation isdeveloped. Thisisthe relationship between vector

![Chapter 18 - Figure 1](../assets/chapter18/_page_17_Figure_1.jpeg)

**Figure 18.9** Time vector diagramsfor a conventional airplane, from *Aircraft Dynamics and Automatic Control* by McRuer, Ashkenas, and Graham (1973). Sideslip angle β is almost nonexistent in the spiral mode. Bank angle dominates in the roll subsidence mode. All motions are of the same order of magnitude in the Dutch roll mode.

ratesof change referred to inertial axes, required for application of Newton'slaw of motion, and vector rates of change as seen on moving axes. A simple vector cross-product connects the two ratesof change. Milne-Thomson'svector equationsof airplane motion on moving axesisof course far more compact than the cartesian form. In *Theoretical Aerodynamics*, Milne-Thomson did extend the vector derivation to the small-perturbation case.

Dyadics are generalized vectors, having nine instead of three components. Rigid-body moments of inertia and angular momenta have particularly simple dyadic forms. Dyadic versionsof the torque or rotational equationsof airplane motion are readily found, but there isno particular advantage to the dyadic form of the ordinary equationsof motion. An advantage does occur for the semirigid case where the relative angular velocities of linked rigid bodiesare computed (Abzug, 1980).

On the other hand, matrix formsof the equationsof airplane motion on moving axes now have a significant role in flight dynamics. This is the result of the marvelous matrix manipulation capability of modern digital computers. The linearized equations of airplane motion are put into matrix form by first expressing the equations in state-variable form. In the state-variable formulation, a first-order differential equation is written for each degree of freedom of the system.

The matrix form is {*x*˙} = [*A*] {*x*} + [*B*] [*u*}, where, for the airplane,

- {*x*} isa *N*-by-1 state vector formed of the perturbation airplane motion states, such as *u*, *v*, and *w*.
- {*x*˙} isthe time derivative of {*x*}.
- [*A*] is a *N*-by-*N* system matrix formed of stability derivatives, such as ∂*X*/∂*u*, mass, and dimensional properties.
- [*B*] is an *N*-by-*M* control matrix formed of control derivativessuch as ∂ *X*/∂δ.
- {*u*} isa *M*-by-1 control vector formed of perturbation control surface angles.

For the perturbation longitudinal equationsa typical state vector {*x*} isthe 5-by-1 vector {*u* α θ *q h*}. A typical control vector {*u*} isthe 1-by-1 vector, hence scalar, {δ*h*}, the stabilizer angle. For the perturbation lateral equations {*x*} istypically the 6-by-1 vector {β φ *p* ψ *r y*}. The control vector isusually the 2-by-1 vector {δ*<sup>a</sup>* δ*r*}.

Modern matrix flight control analysis and synthesis methods generally augment the airplane state vector with control system states and manipulate matrices [*A*] and [*B*] in closed-loop operations. All of the classical Bryan, Gates, Zimmerman, and Perkins analyses for the unaugmented airframe can be carried out with standard computerized matrix manipulations. A prime example is the method of finding transient solutions by forming transition equations from one interval to the next. Transition matrices are computed using large numbers of successive matrix multiplications.

Matrix methodsare fundamental to a number of commercially available flight dynamics computer programs. Systems Technology, Inc., of Hawthorne, California, offers the "Linear System Modeling Program," which does every possible form of linearized stability analysis, including time-vector analysis. The Design, Analysis and Research Corporation of Lawrence, Kansas, produces the "Advanced Aircraft Analysis" program, which does stability and control preliminary design, trim, and flight dynamics. Large general-purpose matrix manipulation computer programssuch as"MATLAB" from MathWorksand "Mathcad" from MatSoft are also commercially available to the stability and control engineer.

The remarksabout the dyadic form of the equationsof airplane motion apply aswell to tensor forms. That is, there is no special advantage in expressing the ordinary equations of rigid-body airplane motion in tensors, as compared with cartesians or vectors. Zipfel (2000) uses a tensor form of the rigid-body equations of airplane motion on moving axes.

### **18.12 Atmospheric Models**

A mathematical model of the earth'satmosphere isneeded for stability and control flight simulation and other computer programs. These programs typically use dimensionless stability derivatives in setting up equations of motion for flight dynamics studies, and stability augmenter and autopilot analyses.

Standard atmospheric mathematical models were published by NACA starting in 1932. A 1955 model covered altitudesup to 65,800 feet (ICAO, 1955). NACA, the U.S. Air Force, and the U.S. Weather Bureau extended that model to an altitude of 400,000 feet (ICAO, 1962). The AIAA publishes a guide to standard atmosphere models (1996). For all its utility, the standard atmospheric model is based on quite simple assumptions: The air is dry, it obeysthe perfect gaslaw, and it isin hydrostatic equilibrium.

Standard atmosphere computer codes for stability and control computer programs normally accept asinputsthe airplane'saltitude and true speed at each computing time. A minimum set of outputs at each computing time would include atmospheric density, Mach number, dynamic pressure, and equivalent airspeed. Additional outputs that could be generated are static pressure and calibrated airspeed.

The standard atmosphere FORTRAN computer code shown in Figure 18.10 represents one of the two methods used in stability and control programs. In this example, air density (RHO) is curve-fitted with exponential functions. Four function fits give satisfactory accuracy over the entire range of −4,000 to 400,000 feet. Speed of sound (ASPE), from which the Mach number iscalculated, requireseight curve-fitted linear equations. The alternate standard atmosphere coding is ordinary interpolation from stored tables of density and speed of sound.

It has become increasingly important to represent wind gusts, shears, downbursts, and vortex encounters in stability and control flight simulation. Early flight simulations relied on a very simplified approach in which an additional gust angle of attack or sideslip is simply added to the values calculated at each instant from the airplane's motions in an inertial space reference.

The sounder approach, now in common use, is an inertially fixed model for the wind environment, including gusts, shears, downbursts, and vortices. A NASA downburst model uses the conservation of mass principle to calculate wind velocity at all points within a downburst (Bray, 1984). A central core is surrounded by an annular mixing region and a region of outflow parallel to the ground (Figure 18.11). In the Bray inertially fixed wind environment, an airplane penetratesthe wind model asit movesalong itspath, just asin reality.

Earlier ad hoc wind shear models were proposed by NASA for flight simulation. A boundary layer shear model represents a low-level temperature inversion overlaid by strong winds. Two additional shear models, with the colorful names of the Logan and Kennedy shears, represent meteorologists' best estimates of conditions existing at those airports during specific airplane wind shear encounters.

In Bernard Etkin's terminology, the Bray downburst model and the NASA shear models are usually used as point atmospheric models, in which variations of local wind velocity over the airplane's dimensions are neglected. Otherwise stated, the airplane is assumed to be vanishingly small with respect to the wavelengths of all spectral components in the turbulent atmosphere. This assumption obviously fails for gust alleviation systems that depend on sensing devices that sample air turbulence ahead of the main structure.

Etkin (1972) provides a thorough study of the finite airplane case, in which local wind velocities vary over the airplane's dimensions. The required mathematics are surprisingly complex because atmospheric turbulence is a random process, and only a statistical, probabilistic

**Figure 18.10** FORTRAN digital computer subroutine for the NASA/USAF/USWB standard atmosphere. Air density (RHO) and speed of sound (ASPE) are curve-fitted in altitude bands from -4,000 to 400,000 feet. The subroutine requires inputs of altitude (ALT) and true speed (VEL). The subroutine outputs density, Mach number (AMACH), dynamic pressure (DYN), and equivalent airspeed (VEKT). (From ACA Systems, Inc. FLIGHT program)

treatment can be made (Ribner, 1956). Local wind velocity isa random function of both space and time. It simplifies things to assume stationarity, homogeneity, isotropy, and Gaussian distributions. Experimental data exist that provide adequate turbulence models for both high altitudesand near the ground, where isotropy doesnot hold.

More exotic atmospheric disturbances are significant for operation at very high altitudes and at hypersonic speeds. Flight disturbances due to temperature shears experienced by the

![Chapter 18 - Figure 1](../assets/chapter18/_page_21_Figure_1.jpeg)

**Figure 18.11** Vertical cross-section through the Bray model of a down-burst. Arrow lengths are proportional to air flow velocity. (From Bray, NASA TM 85969, 1984)

Lockheed SR-71A and the North American XB-70 are discussed in Chapter 11, "High Mach Number Difficulties." In anticipation of a National Aerospace Plane (NASP) that would fly hypersonically, NASA laboratories at Dryden, Marshall, and Langley and the McDonnell Douglas Houston operation collaborated on a sophisticated FORTRAN atmospheric model called the NASP Integrated Atmospheric Model (Schilling, Pickett, and Aubertin, 1993).

The model is suitable for real-time simulations as well as batch programs. It provides global coverage, from the ground to orbital altitudes. The NASP model features of particular stability and control interest are the small-scale perturbations that include continuous turbulence and the "thermodynamic" perturbations of density, pressure, and temperature. Gustsand thermodynamic perturbationscan be selected either in patchesor asdiscrete upsets.

Isolated mountain ridgesthat lie at right anglesto the direction of strong prevailing winds can generate a so-called mountain wave. Air over the top of such a ridge cascades in huge volumesonto the lower terrain to the leeward. It then seemsto bounce off, rising, then falling, and then rising again in a series of diminishing waves, all parallel to the ridge line. A huge rotor, or horizontal vortex, forms to the leeward of the first bounce. The characteristic mountain wave structure is well known to glider pilots, since glider altitude records are set by maneuvering into the rising air of the first bounce. Glider pilots also know to avoid the rotor, whose lower edge generally just brushes ground level. The National Transportation Safety Board (NTSB) concluded that a rotor was a possible cause for at least one airline accident. ThiswasUnited AirlinesFlight 585, a Boeing 737 lost at Colorado Springsin 1991. Variousjet aircraft encounterswith a rotor are modeled by Spilman and Stengel (1995).

Vortex wakes left in the atmosphere by airplanes flying ahead can be a severe hazard, although the principlesfor avoiding vortex wakesare known. Vortex wake fieldscan be modeled for flight simulation (Johnson, Teper, and Rediess, 1974).

## **18.13 Integration Methods and Closed Forms**

Digital computer programs for airplane stability and control time history calculations perform step-by-step integration of the equations of motion. The usual form of the complete equationsof motion for numerical integration on a digital computer is12 simultaneous nonlinear first-order differential equations. Three of the equations produce linear position coordinates, or state components, three produce attitude angles (if Euler angles are used), three produce linear velocity components, and three produce angular velocity components. The 12 airplane coordinatesof motion are referred to asthe airplane'sstate vector.

Accurate, efficient integrating algorithms were a subject of interest among applied mathematiciansfor many yearsbefore stability and control engineersneeded them for computer programming. A well-known text that comparesthe propertiesof many integrating algorithmsis*Introduction to Numerical Analysis* by F. B. Hildebrand, published by McGraw-Hill in 1956.

A fair generalization isthat choice of an integrating algorithm isa trade-off between simplicity, which affects calculation speed, and accuracy. The simplest algorithms, such as Eulerian or "boxcar" integration, require just one calculation pass per computing interval, but they accumulate systematic errors as the time history calculation goes forward. In Eulerian integration, a coordinate such aspitching velocity isprojected forward to the next time interval simply by adding to the present value the product of the present value of pitching acceleration and the time interval length, which isusually of the order of 0.05 second. In general terms, the state vector at the next time interval is the current state vector plusthe product of the state derivative vector and the time interval.

More accurate integration requiresthe calculation of intermediate valuesin order to take the same time step, adding to the computing time but improving accuracy. The best known accurate integration method, in effect a standard for stability and control time history calculations, is the fourth-order Runge-Kutta method. This method can be adapted in FORTRAN to the integration of multiple states, such as the 12 airplane coordinates or state vectors (Melsa and Jones, 1973, and Figure 18.12).

While digital computersbecame available in engineering officesfor stability and control time history calculations around the time of the inertial coupling crisis, or 1950, it was not until many years later that computing speed had increased to the point that the calculations could be made in real time and could thus support flight simulation. One of the earliest such applications was at the Ling-Temco-Vought plant in Arlington, Texas, in the late 1960s. An all-digital flight simulator that went on-line a little later wasNorthrop Aircraft'sLarge Amplitude Simulator, which progressed from analog to hybrid to all-digital in late 1975. With the introduction of real-time digital flight simulation accurate, but slow, integration methods such as the fourth-order Runge-Kutta routine have become something of an obstacle. There isa premium on the development of fast integration methodsthat still have a fair degree of accuracy. Fast but accurate integration methods have been developed all over the United States to meet that need: methods generally starting with a classical scheme and modified by mathematical tinkerers.

The Adam-Bashford method was the starting point for the algorithm used for the projector gimbalsin the Northrop Large Amplitude Simulator. A different set integratesthe airplane equations of motion. Another integration method developed specifically for flight simulation modifies the second-order Runge-Kutta method, replacing the second state derivative vector calculation with a prediction based on a weighted average of previous mid- and endframe values. The modified second-order Runge-Kutta method seems to be almost as accurate as

![Chapter 18 - Figure 1](../assets/chapter18/_page_23_Figure_2.jpeg)

the fourth-order Runge Kutta, while requiring only one calculation of the state derivative vector per interval.

Aerodynamic forcesand momentsare involved in the calculation of the state derivative vector. Thisrequireshuge amountsof table lookup on modern flight simulationsthat cover large Mach number, altitude, and control surface position ranges and uses computer time more than any other part of the computation. Thus, a single calculation of the state derivative vector, asin the modified second-order Runge-Kutta method, isvery efficient for real-time digital flight simulation. A modified second-order Runge-Kutta method was developed in 1972 by Albert F. Myersof NASA; it wasthen improved by him in 1978 for the HIMAT vehicle flight simulation (Figure 18.13).

Another important advance in digital flight simulation is the use of closed-form solutions for the first- and second-order linear differential equations that typically represent analog flight control elements, such as control surface valves and actuators. Closed-form solutions for these elements remove them from the state vector that has to be integrated, reducing the order of that vector to perhapsno more than isrequired by the airplane equationsof motion themselves, or 12. The nonlinearities of control position and velocity limiting are easily represented. This technique is attributed to Juri Kalviste, although there may be other claimantsto priority.

# **18.14 Steady-State Solutions**

Steady-state solutionsto the equationsof airplane motion are defined asmotions with zero values of body axis linear and angular accelerations. Steady straight flight includes climbing, level flight, and diving and allows the airplane to have a nonzero sideslip angle. Steady turning flight allowsconstant valuesof the three body axisangular velocities, yawing, pitching, and rolling.

![Chapter 18 - Figure 1](../assets/chapter18/_page_24_Figure_1.jpeg)

**Figure 18.13** A modified second-order Runge-Kutta integration subroutine developed to run quickly, for use in real-time digital flight simulation. This FORTRAN subroutine was developed by A. F. Myers for NASA'sSIM2 simulation. *X* is the state derivative vector. COMMON input–output statements have been removed for generality. (From ACA Systems, Inc. FLIGHT simulation)

Steady flight conditionsare used asreference valuesfor the perturbationsof linearized analysis (Sec. 18.2). Applications are to root locus, frequency response, covariance propagation, and optimization. Steady flight conditions also establish initial state variables for nonlinear transient analysis, such as landing approaches, gust response, and pilot-initiated maneuvers. Finally, basic stability conditions can be deduced from the control surface angles required for steady flight. For example, spiral instability is implied when opposite aileron angle is required in a steady turn, such as left aileron to hold trim in a steady right turn.

Steady flight solutions are usually obtained for the nonlinear equations of motion by driving to zero selected body axis linear and angular accelerations. Stevens and Lewis (1992) apply a minimization algorithm called the simplex method for trim in steady, straight, symmetric (unsideslipped) flight. A cost function is formed from the sums of squares of the forward, vertical, and pitching accelerations. A multivariable optimization adjusts thrust, elevator angle, and angle of attack to minimize the cost function.

A closed-loop trimming method (Abzug, 1998) is an alternative to the simplex method. The nonlinear state equations are solved in sequence, together with control equations that adjust thrust, angles of attack and sideslip, and control surface angles to minimize accelerations. In the control equations, thrust is adjusted in small steps to minimize longitudinal acceleration, angle of attack is adjusted in small steps to minimize vertical acceleration, elevator angle is adjusted in small steps to minimize pitching acceleration, and so on.

# **18.15 Equations of Motion Extension to Suborbital Flight**

Suborbital flight is flight within the atmosphere but at extremely high altitudes. In this regime, flight speeds are very high, and the curving of constant-altitude flight trajectories around the earth'ssurface addsappreciable centrifugal force to wing lift. Bryan'sequations of rigid-body motion are for flight over a flat earth. Flat-earth equationsof motion generally are inadequate for airplanesthat operate in a suborbital mode.

A derivation of nonlinear airplane equations of motion for the spherical-earth case can be found in Etkin (1972). The main distinction between the spherical- or oblate-earth cases and the classical Bryan flat-earth equations lies in additional kinematic (nondifferential) equations. As in the ordinary flat-earth equations, 12 state equations must be integrated. In the Etkin approach, linear accelerationsare integrated in airplane body axes, producing the usual inertial velocity and angle of attack and sideslip variables. However, this is only one of several possible choices for the linear accelerations. The angular acceleration equations of motion are integrated in airplane body axes, asfor the flat-earth case. Thisisthe only practical choice, since airplane momentsand productsof inertia are constant only in body axes.

Full nonlinear equationsof airplane motion about a spherical or oblate rotating earth were produced somewhat later at Rockwell International in connection with the Space Shuttle Orbiter and still later for studies of the National Aerospace Plane (NASP). The earliest set is found in Rockwell Report SD78-SH-0070, whose authors we have been unable to identify. Six distinct reference axes systems are used. The Rockwell set integrates linear accelerations and velocities in an earth-centered inertial axis system, making transformations to the other axes, such as the body and airport reference sets.

Still another approach wasfollowed at the NASA Dryden Flight Research Center (Powers and Schilling, 1980, 1985) for the Space Shuttle Orbiter, in order to build on an earlier flat-earth 6-DOF computer model. A heading coordinate frame iscentered at the orbiter's center of gravity, with the Z-axispointed to the earth'scenter and the X-axisaligned with the direction of motion. X and Z define the orbit plane through the geocenter. Linear accelerationsand velocitiesare integrated in heading coordinate and earth axesframes, respectively. Vehicle vertical and horizontal velocities in the orbit plane and body axis heading relative to the orbit plane replace the ordinary body axisvelocity coordinatesin the airplane's state vector. Altitude above a reference sphere of equatorial radius, latitude, and longitude replace the ordinary altitude, downrange and cross-range position coordinates in the airplane's state vector. High precision data, such as FORTRAN double precision with 15 significant figures, are needed.

Attitude deviationsfrom the Rockwell/Dryden heading coordinate frame produce Euler angles in the classical sense: yaw, then pitch, then roll. Use of this particular heading coordinate system also for space or re-entry vehicles would produce a consistent set of aerospace flight mechanics axes, which would seem to be an advantage.

The oblate earth version of the equations of airplane motion is sometimes used even when there is no question of hypersonic or suborbital flight operations. This is in flight simulators when one wishes to have only one set of airplane equations for both flying qualities and long-range navigation studies. A single, unified airplane mathematical model for both purposes avoids duplication of costly manned flight simulators and the problem of keeping current two different data bases during airplane development. For simulated flights lasting on the order of hours, correct latitude and longitude coordinates can be calculated asinputsto flight data computers.

The almost incredible capacity of modern digital computers makes it feasible to expend computing capacity by including high-frequency airplane dynamicstermsin the flight simulation of an hours-long navigational mission, as compared with spending engineering time to develop a special simulation without the high-frequency terms. This was the route chosen for the Northrop B-2, according to our best information.

## **18.15.1** *Heading Angular Velocity Correction and Initialization*

The inertial reference for body axisheading angular velocity relative to the orbit plane in the Rockwell/Dryden formulation can be thought of astrue north, defined by the local meridian. However, a local meridian cannot be used as an inertial reference unless its motion asthe earth turnsisaccounted for. Powersand Schilling (1980, 1985) derive this correction.

The earth's atmosphere is carried around with earth rotation, causing side winds relative to the orbit plane. This requires special initialization for starting transient response calculations at zero sideslip. Closed-form initialization formulas are available using initial angle of attack, velocity, and flight path angle.

#### **18.16 Suborbital Flight Mechanics**

The effectsof the earth'scurvature are quite negligible on the airplane modes of interest to the stability and control engineer under ordinary flight conditions. However, some significant effects are expected for the suborbital case. A number of investigators have extended the flat-earth equationsto spherical or oblate modelsin order to examine these effects.

Linearized airplane motionshave been examined in perturbationsfrom great-circle and minor-circle trajectories about a spherical earth (Myers, Klyde, McRuer, and Larson, 1993). In principle, thisisthe same procedure followed by Bairstow (1914) in hisextension of the Bryan equationsof motion to perturbationsfrom steady turning flight. An extra longitudinal mode of motion is found, in addition to the usual short-period and phugoid modes. This is a first-order density mode, also referred to as an *altitude mode*. Aside from this extra complexity, with a typical hypersonic configuration at Mach numbers from 3 to 20 the density mode occasionally couples with real phugoid poles.

There is also an extra lateral-directional real mode, in addition to the usual Dutch roll, spiral, and roll modes. This is called a *kinematic mode*, generally of very long time constant. At some high Mach numbers, the kinematic mode couples into the spiral mode, producing a very low-frequency stable oscillation.

# **18.17 Additional Special Forms of the Equations of Motion**

Trajectory or point-mass equations of airplane motion, lacking the torque or moment equations, have been found useful for flight performance studies. In these applications, angles of attack and sideslip are assumed functions of time or are found in simple closed loops, instead of being the result of attitude adjustments influenced by control surface angles. Trajectory equations of motion have only 6 nonlinear state equations, as compared with 12 for the complete rigid-body equations. The savings in computer time are unimportant with modern digital computers, but there is a conceptual advantage for performance studies in needing to specify only lift, drag, and thrust parameters.

Another special form of the equationsof airplane motion putsthe origin of body axesat an arbitrary location, not necessarily the center of gravity. The first use of such equations seems to have been for fully submerged marine vehicles, such as torpedoes and submarines. With the center of body axesat the center of buoyancy, there are no buoyancy moment changesdue to changesin attitude (Strumpf, 1979). An equivalent set for airplanescame later (Abzug and Rodden, 1993).

Apparent mass and buoyancy terms in the equations of airplane motion are discussed in Chapter 13, "Ultralight and Human-Powered Airplanes." The various special forms of the equations of airplane motion for representing aeroelastic effects are discussed in the next chapter, "The Elastic Airplane."

Equationsof motion for an airplane with an internal moving load that isthen dropped were developed by Bernstein (1998). The motivation is the parachute extraction and dropping of loads from military transport airplanes. A control strategy using feedback from disturbance variablesto the elevator wasable to minimize perturbationsin airplane path and airspeed during the extraction and dropping process.