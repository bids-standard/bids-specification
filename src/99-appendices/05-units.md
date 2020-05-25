# Appendix V: Units

As described in the [units section](../02-common-principles.md#units),
the specification of units MUST follow the
[International System of Units](https://en.wikipedia.org/wiki/International_System_of_Units)
(SI, abbreviated from the French Système international (d'unités)).

The [CMIXF-12](https://people.csail.mit.edu/jaffer/MIXF/CMIXF-12) convention
for encoding units is REQUIRED to achieve maximum portability and limited
variability of representation.
In case that a CMIXF representation of SI units is not possible, you will have
to declare your units as custom units and define them in accompanying JSON
files, as described in the [units section](../02-common-principles.md#units).
Earlier versions of the BIDS standard listed the following Unicode symbols, and
these are still included for backwards compatibility:

1.  `U+00B5` (µ)
1.  `U+00B0` (°)
1.  `U+2126` (Ω).

It is REQUIRED that units be CMIXF-12 compliant or among these three Unicode
characters.

Units MUST consist of the `unit symbol` with an optionally accompanying
`prefix symbol` (see table below). Appropriate upper- or lower- casing MUST
be applied as declared by CMIXF-12.

For cases that are unspecified by this appendix, or the
[units section](../02-common-principles.md#units), the
[CMIXF-12](https://people.csail.mit.edu/jaffer/MIXF/CMIXF-12) convention
applies.

Examples:

1.  `uV` or `µV` are permissible, but NOT: `microV`, `µvolt`, `1e-6V`, etc.
1.  Combinations of units are allowed, e.g., `V/us` for the [Slew rate](https://en.wikipedia.org/wiki/Slew_rate)

| Unit name      | Unit symbol       | Quantity name                              |
| -------------- | ----------------- | ------------------------------------------ |
| metre          | m                 | length                                     |
| kilogram       | kg                | mass                                       |
| second         | s                 | time                                       |
| ampere         | A                 | electric current                           |
| kelvin         | K                 | thermodynamic temperature                  |
| mole           | mol               | amount of substance                        |
| candela        | cd                | luminous intensity                         |
| radian         | rad               | angle                                      |
| steradian      | sr                | solid angle                                |
| hertz          | Hz                | frequency                                  |
| newton         | N                 | force, weight                              |
| pascal         | Pa                | pressure, stress                           |
| joule          | J                 | energy, work, heat                         |
| watt           | W                 | power, radiant flux                        |
| coulomb        | C                 | electric charge or quantity of electricity |
| volt           | V                 | voltage (electrical potential), emf        |
| farad          | F                 | capacitance                                |
| ohm            | Ohm or Ω (U+2126) | resistance, impedance, reactance           |
| siemens        | S                 | electrical conductance                     |
| weber          | Wb                | magnetic flux                              |
| tesla          | T                 | magnetic flux density                      |
| henry          | H                 | inductance                                 |
| degree Celsius | oC or °C (U+00B0) | temperature relative to 273.15 K           |
| lumen          | lm                | luminous flux                              |
| lux            | lx                | illuminance                                |
| becquerel      | Bq                | radioactivity (decays per unit time)       |
| gray           | Gy                | absorbed dose (of ionizing radiation)      |
| sievert        | Sv                | equivalent dose (of ionizing radiation)    |
| katal          | kat               | catalytic activity                         |

## Prefixes

### Multiples

| Prefix name                                 | Prefix symbol | Factor          |
| ---------------------------------------------------------- | ---------------------------- | ------------------------------- |
| [deca](https://www.wikiwand.com/en/Deca-)   | da            | 10<sup>1</sup>  |
| [hecto](https://www.wikiwand.com/en/Hecto-) | h             | 10<sup>2</sup>  |
| [kilo](https://www.wikiwand.com/en/Kilo-)   | k             | 10<sup>3</sup>  |
| [mega](https://www.wikiwand.com/en/Mega-)   | M             | 10<sup>6</sup>  |
| [giga](https://www.wikiwand.com/en/Giga-)   | G             | 10<sup>9</sup>  |
| [tera](https://www.wikiwand.com/en/Tera-)   | T             | 10<sup>12</sup> |
| [peta](https://www.wikiwand.com/en/Peta-)   | P             | 10<sup>15</sup> |
| [exa](https://www.wikiwand.com/en/Exa-)     | E             | 10<sup>18</sup> |
| [zetta](https://www.wikiwand.com/en/Zetta-) | Z             | 10<sup>21</sup> |
| [yotta](https://www.wikiwand.com/en/Yotta-) | Y             | 10<sup>24</sup> |

### Submultiples

| Prefix name                                 | Prefix symbol   | Factor           |
| ------------------------------------------- | --------------- | ---------------- |
| [deci](https://www.wikiwand.com/en/Deci-)   | d               | 10<sup>-1</sup>  |
| [centi](https://www.wikiwand.com/en/Centi-) | c               | 10<sup>-2</sup>  |
| [milli](https://www.wikiwand.com/en/Milli-) | m               | 10<sup>-3</sup>  |
| [micro](https://www.wikiwand.com/en/Micro-) | u or µ (U+00B5) | 10<sup>-6</sup>  |
| [nano](https://www.wikiwand.com/en/Nano-)   | n               | 10<sup>-9</sup>  |
| [pico](https://www.wikiwand.com/en/Pico-)   | p               | 10<sup>-12</sup> |
| [femto](https://www.wikiwand.com/en/Femto-) | f               | 10<sup>-15</sup> |
| [atto](https://www.wikiwand.com/en/Atto-)   | a               | 10<sup>-18</sup> |
| [zepto](https://www.wikiwand.com/en/Zepto-) | z               | 10<sup>-21</sup> |
| [yocto](https://www.wikiwand.com/en/Yocto-) | y               | 10<sup>-24</sup> |
