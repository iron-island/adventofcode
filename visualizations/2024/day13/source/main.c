// Include the most common headers from the C standard library
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Include the main libnx system header, for Switch development
#include <switch.h>

// See also libnx pad.h / hid.h.

// Screen grid macros
#define HORIZONTAL_EDGE   "="
#define VERTICAL_EDGE     "|"
#define UPPERLEFT_CORNER  "+"
#define UPPERRIGHT_CORNER "+"
#define LOWERLEFT_CORNER  "+"
#define LOWERRIGHT_CORNER "+"

#define INIT_ROW_GRID_LINES 17
#define INIT_COL_GRID_LINES 5
#define GRID_LINES_ROWS 25
#define GRID_LINES_COLS 69

#define CLAW_TOP "\\ /"
#define CLAW_MID   "X"
#define CLAW_BOT  "/ \\"
#define CLAW_ROW 29
#define CLAW_COL 39

// Main program entrypoint
int main(int argc, char* argv[])
{
    // This example uses a text console, as a simple way to output text to the screen.
    // If you want to write a software-rendered graphics application,
    //   take a look at the graphics/simplegfx example, which uses the libnx Framebuffer API instead.
    // If on the other hand you want to write an OpenGL based application,
    //   take a look at the graphics/opengl set of examples, which uses EGL instead.
    consoleInit(NULL);

    // Configure our supported input layout: a single player with standard controller styles
    padConfigureInput(1, HidNpadStyleSet_NpadStandard);

    // Initialize the default gamepad (which reads handheld mode inputs as well as the first connected controller)
    PadState pad;
    padInitializeDefault(&pad);

    //Matrix containing the name of each key. Useful for printing when a key is pressed
    char keysNames[28][32] = {
        "A", "B", "X", "Y",
        "StickL", "StickR", "L", "R",
        "ZL", "ZR", "Plus", "Minus",
        "Left", "Up", "Right", "Down",
        "StickLLeft", "StickLUp", "StickLRight", "StickLDown",
        "StickRLeft", "StickRUp", "StickRRight", "StickRDown",
        "LeftSL", "LeftSR", "RightSL", "RightSR",
    };

    u32 kDownOld = 0, kHeldOld = 0, kUpOld = 0; //In these variables there will be information about keys detected in the previous frame

    int i;
    int machine_num, total_machines;
    int ax, ay;
    int bx, by;
    int px, py;
    int curr_x, curr_y;
    int old_i, old_x, old_y;
    int tokens, prizes;
    int grid_x_offset, grid_y_offset;

    // Screen grid variables
    // +10 for offsets, +1 on cols for null terminator
    char sliced_grid_line[GRID_LINES_COLS+1] = "";
    char grid_lines[GRID_LINES_ROWS+10][GRID_LINES_COLS+10+1] = {
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     " . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     " . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     " . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
     " . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ", 
     "    .         .         .         .         .         .         .         .    ", 
     "    .         .         .         .         .         .         .         .    ", 
    };

    // TODO:
    machine_num = 1;
    total_machines = 1;
    ax = 94;
    ay = 34;
    bx = 22;
    by = 67;
    px = 8400;
    py = 5400;
    curr_x = 0;
    curr_y = 0;
    old_i = -1;
    old_x = 0;
    old_y = 0;
    tokens = 0;
    prizes = 0;
    grid_x_offset = 0;
    grid_y_offset = 0;

    printf("\x1b[1;1H Advent of Code 2024 Day 13: Claw Contraption");
    printf("\x1b[2;1H Instructions: Press A/B to move right/forward");
    printf("\x1b[3;1H               Press X/Y to cancel A/B movements (no token refunds!)");

    printf("\x1b[4;1H   Machine %d of %d", machine_num, total_machines);
    printf("\x1b[5;1H     Button A: X+%d, Y+%d", ax, ay);
    printf("\x1b[6;1H     Button B: X+%d, Y+%d", bx, by);
    printf("\x1b[7;1H     Prize: X=%d, Y=%d", px, py);

    printf("\x1b[9;1H   Current (X, Y) = (%d, %d)", curr_x, curr_y);
    printf("\x1b[10;1H   Tokens spent = %d", tokens);
    printf("\x1b[11;1H   Prizes caught = %d", prizes);
    printf("\x1b[12;1H   No button pressed yet");

    // Main loop
    while(appletMainLoop())
    {
        // Scan the gamepad. This should be done once for each frame
        padUpdate(&pad);

        // padGetButtonsDown returns the set of buttons that have been
        // newly pressed in this frame compared to the previous one
        u64 kDown = padGetButtonsDown(&pad);

        // padGetButtons returns the set of buttons that are currently pressed
        u64 kHeld = padGetButtons(&pad);

        // padGetButtonsUp returns the set of buttons that have been
        // newly released in this frame compared to the previous one
        u64 kUp = padGetButtonsUp(&pad);

        if (kDown & HidNpadButton_Plus)
            break; // break in order to return to hbmenu

        // Do the keys printing only if keys have changed
        if (kDown != kDownOld || kHeld != kHeldOld || kUp != kUpOld)
        {
            // Clear console
            consoleClear();

            // Rewrite lines after clearing the whole screen
            printf("\x1b[1;1H Advent of Code 2024 Day 13: Claw Contraption");
            printf("\x1b[2;1H Instructions: Press A/B to move right/forward");
            printf("\x1b[3;1H               Press X/Y to cancel A/B movements (no token refunds!)");

            printf("\x1b[4;1H   Machine %d of %d", machine_num, total_machines);
            printf("\x1b[5;1H     Button A: X+%d, Y+%d", ax, ay);
            printf("\x1b[6;1H     Button B: X+%d, Y+%d", bx, by);
            printf("\x1b[7;1H     Prize: X=%d, Y=%d", px, py);

            printf("\x1b[9;1H   Current (X, Y) = (%d, %d)", curr_x, curr_y);
            printf("\x1b[10;1H   Tokens spent = %d", tokens);
            printf("\x1b[11;1H   Prizes caught = %d", prizes);
            if (old_i > -1) {
                printf("\x1b[12;1H   Button %s pressed, position updated: (%d, %d) -> (%d, %d)", keysNames[old_i], old_x, old_y, curr_x, curr_y);
            }
            
            // Check if some of the keys are down, held or up
            // Max index of 3 for A, B, X, Y
            for (i = 0; i < 4; i++)
            {
                if (kDown & BIT(i)){
                    //printf("%s down\n", keysNames[i]);

                    old_i = i;
                    old_x = curr_x;
                    old_y = curr_y;
                    if (i == 0) { // Button A pressed
                        curr_x = curr_x + ax;
                        curr_y = curr_y + ay;
                        tokens = tokens + 3;
                    }
                    else if (i == 1) { // Button B pressed
                        curr_x = curr_x + bx;
                        curr_y = curr_y + by;
                        tokens = tokens + 1;
                    }
                    else if (i == 2) { // Button X pressed
                        curr_x = curr_x - ax;
                        curr_y = curr_y - ay;
                    }
                    else if (i == 3) { // Button Y pressed
                        curr_x = curr_x - bx;
                        curr_y = curr_y - by;
                    }

                    // Only 1 button can be pressed at a time, so exit loop
                    // This means button priorities are A, B, X, Y
                    break;
                }
                //if (kHeld & BIT(i)) printf("%s held\n", keysNames[i]);
                //if (kUp & BIT(i)) printf("%s up\n", keysNames[i]);
            }
        }

        // Check current position vs prize position
        if ((curr_x > px) || (curr_y > py)) {
            // Overshot and did not get the prize
            printf("\x1b[13;1H   Went beyond the prize! Go back with X/Y!");
        }
        else if ((curr_x == px) && (curr_y == py)) {
            // Got the prize
            printf("\x1b[13;1H   Congratulations! You caught a prize!");
            prizes = prizes + 1;

            // TODO: Print option to go to next machine
        }

        // Print grid lines
        // TODO: handle negative coordinates
        grid_x_offset = curr_x % 10;
        grid_y_offset = curr_y % 10;
        for (i = 0 ; i < GRID_LINES_ROWS; i++) {
            printf("\x1b[%d;%dH", INIT_ROW_GRID_LINES+i, INIT_COL_GRID_LINES);
            snprintf(sliced_grid_line, GRID_LINES_COLS+1, "%s", grid_lines[i+grid_x_offset]+grid_y_offset);
            printf("%s", sliced_grid_line);
        }

        // Print claw
        printf("\x1b[%d;%dH%s", CLAW_ROW-1, CLAW_COL-1, CLAW_TOP);
        printf("\x1b[%d;%dH%s", CLAW_ROW, CLAW_COL, CLAW_MID);
        printf("\x1b[%d;%dH%s", CLAW_ROW+1, CLAW_COL-1, CLAW_BOT);

        // Print horizontal borders
        // Upper left corner
        printf("\x1b[%d;%dH", INIT_ROW_GRID_LINES-1, INIT_COL_GRID_LINES-1);
        printf(UPPERLEFT_CORNER);
        // Top border
        for (i = 0; i < GRID_LINES_COLS; i++){
            printf(HORIZONTAL_EDGE);
        }
        // Upper right corner
        printf(UPPERRIGHT_CORNER);
        // Lower left corner
        printf("\x1b[%d;%dH", INIT_ROW_GRID_LINES+GRID_LINES_ROWS, INIT_COL_GRID_LINES-1);
        printf(LOWERLEFT_CORNER);
        // Bottom border
        for (i = 0; i < GRID_LINES_COLS; i++){
            printf(HORIZONTAL_EDGE);
        }
        // Lower right corner
        printf(LOWERRIGHT_CORNER);

        // Print vertical borders
        for (i = 0; i < GRID_LINES_ROWS; i++){
            // Left border
            printf("\x1b[%d;%dH%s", INIT_ROW_GRID_LINES+i, INIT_COL_GRID_LINES-1, VERTICAL_EDGE);
            // Right border
            printf("\x1b[%d;%dH%s", INIT_ROW_GRID_LINES+i, INIT_COL_GRID_LINES+GRID_LINES_COLS, VERTICAL_EDGE);
        }

        // Set keys old values for the next frame
        kDownOld = kDown;
        kHeldOld = kHeld;
        kUpOld = kUp;

        // Update the console, sending a new frame to the display
        consoleUpdate(NULL);
    }

    // Deinitialize and clean up resources used by the console (important!)
    consoleExit(NULL);
    return 0;
}
