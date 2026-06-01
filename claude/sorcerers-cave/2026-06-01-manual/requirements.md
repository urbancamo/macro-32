# Sorcerers Cave - Interactive Manual

We need an interactive manual for the game Sorcerer's Cave. It should be available via a help menu.
The manual should contain:
 
 - an index of topics
 - a chart of the ascii characters used to represent creatures, treasure and artifacts
 - a glossary of artifacts and their effects
 - a table of creature attributes
 - a how-to guide for new adventurers
 - the complete original game manual available as a separate, complete text.

Before creating the help files, you'll need to decide on the best representation for a VAX/VMS Macro-32 program.
It could even be an interactive help file in the VAX/VMS help system, as a standalone help file, if that makes sense.

# Creating an implementation plan
 
 - I'm not sure what the best format for the file should be, you should do research on this as there is rich support
   for structured data at the file level.
 - make use of SMG$ routines to navigate the data, using reverse highlight and arrow keys together with appropriate
   shortcuts.
 - it might be best to create the format using markdown, and interpret the markdown. Not sure.
 
Present the implementation plan for review before proceeding.


T