# Appendix V: Units

As described in the [Units](../02-common-principles.md#units),
the specification of units SHOULD follow the
[International System of Units](https://en.wikipedia.org/wiki/International_System_of_Units)
(SI, abbreviated from the French Système international (d'unités)).

The [CMIXF-12](https://people.csail.mit.edu/jaffer/MIXF/CMIXF-12) convention
for encoding units is RECOMMENDED to achieve maximum portability and limited
variability of representation.
If a CMIXF-12 representation of a unit is not possible, the unit can be declared
as custom units and defined in an accompanying JSON file, as described in the
[units section](../02-common-principles.md#units).
Earlier versions of the BIDS standard listed the following Unicode symbols, and
these are still included for backwards compatibility:

1.  [`U+03BC` (μ)](https://codepoints.net/U+03BC) or [`U+00B5` (µ)](https://codepoints.net/U+00B5)
1.  [`U+03A9` (Ω)](https://codepoints.net/U+03A9) or [`U+2126` (Ω)](https://codepoints.net/U+2126)
1.  [`U+00B0` (°)](https://codepoints.net/U+00B0)

Note that for the first two entries in this list, two characters are permissible
for each, but the first character in each entry is preferred, per Unicode rules
(see the section on "Duplicated Characters" on page 11 in the
[unicode report](https://www.unicode.org/reports/tr25/)).

It is RECOMMENDED that units be CMIXF-12 compliant or among these five Unicode
characters.
Please note the appropriate upper- or lower- casing when using CMIXF-12.

For cases that are unspecified by this appendix or the[units section](../02-common-principles.md#units),
the [CMIXF-12](https://people.csail.mit.edu/jaffer/MIXF/CMIXF-12) convention
applies.

You can use the [cmixf Python package](https://github.com/sensein/cmixf) to
check whether your formatting is compliant.

Examples for CMIXF-12 (including the five unicode symbols mentioned above):

1.  Different formatting of "micro Volts":
    1.  RECOMMENDED: `uV` or `µV`
    1.  NOT RECOMMENDED: `microV`, `µvolt`, `1e-6V`, etc.

1.  Combinations of units:
    1.  RECOMMENDED: `V/us` for the [Slew rate](https://en.wikipedia.org/wiki/Slew_rate)
    1.  NOT RECOMMENDED: `volts per microsecond`

## Unit table

| Unit name      | Unit symbol | Quantity name                              |
| -------------- | ----------- | ------------------------------------------ |
| metre          | m           | length                                     |
| kilogram       | kg          | mass                                       |
| litre (liter)  | L           | volume                                     |
| second         | s           | time                                       |
| ampere         | A           | electric current                           |
| kelvin         | K           | thermodynamic temperature                  |
| mole           | mol         | amount of substance                        |
| candela        | cd          | luminous intensity                         |
| radian         | rad         | angle                                      |
| steradian      | sr          | solid angle                                |
| hertz          | Hz          | frequency                                  |
| newton         | N           | force, weight                              |
| pascal         | Pa          | pressure, stress                           |
| joule          | J           | energy, work, heat                         |
| watt           | W           | power, radiant flux                        |
| coulomb        | C           | electric charge or quantity of electricity |
| volt           | V           | voltage (electrical potential), emf        |
| farad          | F           | capacitance                                |
| ohm            | Ohm         | resistance, impedance, reactance           |
| siemens        | S           | electrical conductance                     |
| weber          | Wb          | magnetic flux                              |
| tesla          | T           | magnetic flux density                      |
| henry          | H           | inductance                                 |
| degree Celsius | oC          | temperature relative to 273.15 K           |
| lumen          | lm          | luminous flux                              |
| lux            | lx          | illuminance                                |
| becquerel      | Bq          | radioactivity (decays per unit time)       |
| gray           | Gy          | absorbed dose (of ionizing radiation)      |
| sievert        | Sv          | equivalent dose (of ionizing radiation)    |
| katal          | kat         | catalytic activity                         |

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

| Prefix name                                 | Prefix symbol | Factor           |
| ------------------------------------------- | ------------- | ---------------- |
| [deci](https://www.wikiwand.com/en/Deci-)   | d             | 10<sup>-1</sup>  |
| [centi](https://www.wikiwand.com/en/Centi-) | c             | 10<sup>-2</sup>  |
| [milli](https://www.wikiwand.com/en/Milli-) | m             | 10<sup>-3</sup>  |
| [micro](https://www.wikiwand.com/en/Micro-) | u             | 10<sup>-6</sup>  |
| [nano](https://www.wikiwand.com/en/Nano-)   | n             | 10<sup>-9</sup>  |
| [pico](https://www.wikiwand.com/en/Pico-)   | p             | 10<sup>-12</sup> |
| [femto](https://www.wikiwand.com/en/Femto-) | f             | 10<sup>-15</sup> |
| [atto](https://www.wikiwand.com/en/Atto-)   | a             | 10<sup>-18</sup> |
| [zepto](https://www.wikiwand.com/en/Zepto-) | z             | 10<sup>-21</sup> |
| [yocto](https://www.wikiwand.com/en/Yocto-) | y             | 10<sup>-24</sup> |
