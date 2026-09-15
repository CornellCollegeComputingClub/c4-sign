# C4 Sign Hardware

This directory contains 3D models for components of the C4 Sign.
The files are provided in `.step` format and in `.3mf` format for ease of use with PrusaSlicer. The orientations of the parts in the `.3mf` files is what you should follow if you intend to print the parts from the `.step` files.

![A 3D rendering of the C4 sign enclosure, wall mount, and table mount.](../docs/images/drawing.png)

## CAD Models
Onshape was used to create the 3D models.
You can view, copy, and export the files from the Onshape document [here](https://cad.onshape.com/documents/50a6dd1d51ea1e299c3249ce/w/c5fab5a3d385c6eac783e8bf/e/fc7822103a772480f21f1e05).

## Electrical
Files are in `./electrical`. This directory contains KiCad documents for the level-shifting PCB that attaches to the Raspberry Pi. The KiCad files can be opened with KiCad 9.0 and later. The main project file is `./electrical/LED Sign Breakout.kicad_pro`. A PDF of the schematic is located at `./electrical/LED Sign Breakout.pdf`. It's not a very good schematic.

> [!WARNING]
> When I designed this PCB, I wasn't paying as much attention as I should have. I accidentally wired the button pins to GPIO 20 and GPIO 21. This may have been a mistake as GPIO 20 and 21 are associated with the RPi's PCM peripheral. The PCM peripheral is actively used in our software to send display information to the LED matrix via GPIO 18 (PCM CLK). I'm a little unsure whether this would make the buttons unusable when the sign is running. When I first added the button functionality (after the PCB had already been installed) I kept getting errors. These later turned out to be errors relating to using the `gpiozero` library inside a Python `venv`. I had to recreate the venv on the RPi with the `--system-site-packages` flag. This worked, but only after I had cut the traces to GPIO 20 and 21 and rewired the buttons to GPIO 16 and GPIO 12.

![The level shifting bridge PCB.](../docs/images/bridge.png)

### Bill of Materials
All necessary parts are described in the KiCad Project.

<details>
  <summary>JLCPCB Ordering Instructions</summary>
  TODO: FIND PREVIOUS JLCPCB ORDER DETAILS AND WRITE THEM HERE
</details>


## Enclosure
Files are in `./enclosure`. This directory contains the `.step` and `.3mf` files for the front and back of the enclosure. The enclosure can be hung on a wall or sat on a table.

### Bill of Materials

#### Printables
| Item | Quantity | .step file | .3mf file |
| :-- | -: | :--: | :--: |
| Face | 1 | `./enclosure/EnclosureDesign-Face.step` | `./enclosure/EnclosureDesign-Face.3mf` |
| Back | 1 | `./enclosure/EnclosureDesign-Back.step` | `./enclosure/EnclosureDesign-Back.3mf` |
| Hook | 1 | `./enclosure/EnclosureDesign-Hook.step` | `./enclosure/EnclosureDesign-Hook.3mf` |

#### Non-printables
| Item | Quantity | Description |
| :-- | --: | :-- |
| Raspberry Pi Model 4 B | 1 | |
| Raspberry Pi Active Cooler | 1 | [Product Link](https://thepihut.com/products/dual-fan-heatsink-case-for-raspberry-pi-4) |
| 16x2 I2C HD44780 LCD | 1 | [Product Link](https://www.amazon.com/HiLetgo-HD44780-I2C1602-Interface-Backlight/dp/B07W5KC65S?th=1) |
| 16mm Panel Mount Momentary Pushbutton | 1 | [Product Link](https://www.adafruit.com/product/1505) |
| Jumper Wires crimped for arcade buttons and 2.54mm pins | 1 | [Product Link](https://www.adafruit.com/product/1152) |
| #6-32 5/8" Socket Head Cap Screw | 4 | For securing face of enclosure to back. |
| #6-32 Hex Nut | 4 | For securing face of enclosure to back. |
| M2.5 22mm Screw | 4 | For securing LCD module to back. The screws can be anywhere from ~21mm to 38mm in length. |
| M2.5 Hex Nut | 4 | For securing LCD module to back. |
| 3/8" Vinyl Self Adhesive Protective Pad | 4 | [Product Link](https://www.acehardware.com/departments/home-and-decor/furniture/protective-furniture-pads/5044524) |
| Level shifter PCB | 1 | See [Electrical](#electrical) |
| Command Strip | 1 | Used to adhere hook to wall.|

## Wall Mount
Files are in `./wallmount`. This directory contains the `.step` and `.3mf` files for mounting the C4 sign to a wall.

### Bill of Materials

#### Printables
| Item | Quantity | .step file | .3mf file |
| :-- | -: | :--: | :--: |
| Support Hook | 3 | `./wallmount/SupportHook.step` | `./wallmount/SupportHook.3mf` |

#### Non-printables
| Item | Quantity | Description |
| :-- | --: | :-- |
| Command Strip | 3 | Used to attach support hooks to walls |
| 8" Steel Bar | 1 | Used to keep bottom two support hooks attached. 1/4" by 1/4" square steel bar with ground edges. |

## Table Mount
Files are in `./tablemount`. This directory contains the `.step` and `.3mf` files for displaying the C4 sign on a table.

### Bill of Materials

#### Printables
| Item | Quantity | .step file | .3mf file |
| :-- | -: | :--: | :--: |
| Top Claw | 1 | `./tablemount/SignTableHolder-BackFootAndClaw.step` | `./tablemount/SignStandClawBackFoot.3mf` |
| Back Foot | 1 | `./tablemount/SignTableHolder-BackFootAndClaw.step` | `./tablemount/SignStandClawBackFoot.3mf`|
| Vertical Tee | 1 | `./tablemount/SignTableHolder-Tees.step`| `./tablemount/SignStandTees.3mf`|
| Front Tee | 1 | `./tablemount/SignTableHolder-Tees.step`| `./tablemount/SignStandTees.3mf`|
| Front Foot | 2 | `./tablemount/SignTableHolder-FrontFeet.step`| `./tablemount/SignStandFrontFeet.3mf`|

#### Non-printables
| Item | Quantity | Description |
| :-- | --: | :-- |
| Vertical Bar | 1 | 1/4" square steel bar cut to 11.85" with edges ground. |
| Transverse Bar | 1 | 1/4" square steel bar cut to 8" to 9" with edges ground. |
| Length Bar | 1 | 1/4" square steel bar cut to 6.85" with edges ground. |
| Hypotenuse Bar | 1 | 1/4" square steel bar cut to 12.85" with edges ground. |