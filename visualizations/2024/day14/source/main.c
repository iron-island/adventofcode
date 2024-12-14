// Include the most common headers from the C standard library
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "input14.h"

// Include the main libnx system header, for Switch development
#include <switch.h>
#include <math.h>

// See also libnx pad.h / hid.h.

#define VISUALIZATION_LENGTH 80
#define MAX_ROW 102
#define MAX_COL 100

#define HORIZONTAL_EDGE   "="
#define VERTICAL_EDGE     "|"
#define UPPERLEFT_CORNER  "+"
#define UPPERRIGHT_CORNER "+"
#define LOWERLEFT_CORNER  "+"
#define LOWERRIGHT_CORNER "+"

#define INIT_ROW_GRID_LINES 7
#define INIT_COL_GRID_LINES 5
#define GRID_LINES_ROWS 35
#define GRID_LINES_COLS 69

#define WINDOW_ROW_OFFSET 28
#define WINDOW_COL_OFFSET 0

// Print borders
void print_borders(){
    int i;

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
}

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
    //char keysNames[28][32] = {
    //    "A", "B", "X", "Y",
    //    "StickL", "StickR", "L", "R",
    //    "ZL", "ZR", "Plus", "Minus",
    //    "Left", "Up", "Right", "Down",
    //    "StickLLeft", "StickLUp", "StickLRight", "StickLDown",
    //    "StickRLeft", "StickRUp", "StickRRight", "StickRDown",
    //    "LeftSL", "LeftSR", "RightSL", "RightSR",
    //};

    //u32 kDownOld = 0, kHeldOld = 0, kUpOld = 0; //In these variables there will be information about keys detected in the previous frame

    int num;
    int curr_num;
    int i;
    int n_x, n_y;
    int row, col;

    //int final_pos[500][2];

    // TODO: Dynamically compute base on input
    num = 8087;
    //curr_num = 8087 - VISUALIZATION_LENGTH;
    curr_num = 8087;

    printf("\x1b[1;1H Advent of Code 2024 Day 14: Restroom Redoubt");

    printf("\x1b[2;1H Seconds: %d of %d", curr_num, num);
    printf("\x1b[3;1H");
    for (i = 0; i < VISUALIZATION_LENGTH; i++){
        printf(".");
    }

    // Main loop
    while(appletMainLoop())
    {
        // Scan the gamepad. This should be done once for each frame
        padUpdate(&pad);

        // padGetButtonsDown returns the set of buttons that have been
        // newly pressed in this frame compared to the previous one
        u64 kDown = padGetButtonsDown(&pad);

        // padGetButtons returns the set of buttons that are currently pressed
        //u64 kHeld = padGetButtons(&pad);

        // padGetButtonsUp returns the set of buttons that have been
        // newly released in this frame compared to the previous one
        //u64 kUp = padGetButtonsUp(&pad);

        if (kDown & HidNpadButton_Plus)
            break; // break in order to return to hbmenu

        // Do the keys printing only if keys have changed
        //if (kDown != kDownOld || kHeld != kHeldOld || kUp != kUpOld)
        //{
        // Clear console
        consoleClear();

        // Read the sticks' position
        HidAnalogStickState analog_stick_l = padGetStickPos(&pad, 0);
        HidAnalogStickState analog_stick_r = padGetStickPos(&pad, 1);

        // Print the sticks' position
        printf("\x1b[4;1H%04d; %04d         %04d; %04d", analog_stick_l.x, analog_stick_l.y, analog_stick_r.x, analog_stick_r.y);

        // Rewrite lines after clearing the whole screen
        printf("\x1b[1;1H Advent of Code 2024 Day 14: Restroom Redoubt");

        printf("\x1b[2;1H Seconds: %d of %d", curr_num, num);
        printf("\x1b[3;1H");
        for (i = 0; i < (curr_num - (num - VISUALIZATION_LENGTH)); i++){
            printf("|");
        }
        for (i = curr_num; i < num; i++){
            printf(".");
        }


        // Draw empty grid
        for (row = 0; row < GRID_LINES_ROWS; row++){
            printf("\x1b[%d;%dH", row+INIT_ROW_GRID_LINES, INIT_COL_GRID_LINES);
            for (col = 0; col < GRID_LINES_COLS; col++){
                printf(".");
            }
        }

        // Compute positions and draw robot if in grid window
        for (i = 0; i < 500; i++){
            n_x = (robots[i][0] + curr_num*robots[i][2]) % (MAX_COL+1);
            n_y = (robots[i][1] + curr_num*robots[i][3]) % (MAX_ROW+1);

            //final_pos[i][0] = n_x;
            //final_pos[i][1] = n_y;

            if ((n_x > WINDOW_COL_OFFSET) && (n_x < (WINDOW_COL_OFFSET + GRID_LINES_COLS)) &&
                (n_y > WINDOW_ROW_OFFSET) && (n_y < (WINDOW_ROW_OFFSET + GRID_LINES_ROWS))) {
                    printf("\x1b[%d;%dH#", n_y-WINDOW_ROW_OFFSET+INIT_ROW_GRID_LINES, n_x-WINDOW_COL_OFFSET+INIT_COL_GRID_LINES);
            }
        }

        // Print borders
        print_borders();
        
        // Update the console, sending a new frame to the display
        consoleUpdate(NULL);
    }

    // Deinitialize and clean up resources used by the console (important!)
    consoleExit(NULL);
    return 0;
}
