# High-Level Requirements

 - We want to be able to show a visualization of the current tunnel or chamber the party is in. This should be drawn 
   as ascii art or better using SMG$ to draw line art, if that is possible.
 - We want a navigable high level map view of the entire dungeon.

# Requirements

Implement this feature without asking questions or user intervention. You can test the feature by running the
application on the VAX, capturing the output and verifying correctness. Do not stop until the feature is complete.
If required, rearrange the display so the visualization fits with everything else on an 80x24 terminal.
The mapping will require a separate 'screen', so can use the full terminal area.

## General
 
1. Staircases should be drawn, probably using a D or U symbol, within the tunnel or chamber.
2. Use single letters or mnemonics for creatures, treasure or hazards. If single letters do not provide uniqueness,
   use 3 character mnemonics.

## Tunnels

- a tunnel should be shown as a corridor with appropriate exits, north, south, east and west.

Example:
```
        |   |
    ----+   +----
          U
    ----+   +----
        |   |
```
_A tunnel with exits North, South, East and West and a staircase up._

## Chamber

1. Creatures should be shown as a single letter, where possible the first letter of their name. Put creature letters
   top-left.
2. Chambers should be show as a rectangle, with exits drawn north, south, east and west. Put Up and Down letters
   top-right.
3. Treasure should be shown as a single letter, where possible the first letter of their name. Put treasure 
   bottom-left.
4. Hazards should be shown bottom right.
5. You could display the party members in the centre of the chamber.

Example:
```
              |   |
         +----+   +----+
         |  W       D  |
    -----+             +----
               D M
    -----+             +----
         |  G F     T  |
         +----+   +----+
              |   |
```

_A chamber with exits NSEW and Down, Containing a Wizard. Gold and Magic Flute. A Trap is shown but the party
does not fall down it because it contains a dwarf_

## Map view

 - Implement a map view that shows the connected tunnels and chambers as a separate display.
 - You should be able to navigate up and down levels, and it should be obvious how the levels connect.
 - The user will need to be able to scroll the map as it may not fit on the display fully.
 - You should display the current party location.
 - There is no requirement to display treasure, creatures or hazards.
 - Distinguish the special chamber locations, such as the Gateway, Viper Pit etc.
