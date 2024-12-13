// Include the most common headers from the C standard library
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Include the main libnx system header, for Switch development
#include <switch.h>
#include <math.h>

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

#define PRIZE_MID "{*}"

#define DELAY_MS 100

void wait_delay(){
    // Tick variables, based on:
    //   https://github.com/switchbrew/switch-examples/tree/master/graphics/opengl/es2gears/source/main.c
    double t;
    static u64 origTicks = UINT64_MAX;

    while (1) {
        if (origTicks == UINT64_MAX)
           origTicks = armGetSystemTick();
        u64 ticksElapsed = armGetSystemTick() - origTicks;
        //t = (ticksElapsed * 625 / 12) / 1000000000.0; // t in seconds?
        t = (ticksElapsed * 625 / 12) / 1000000.0; // t in milliseconds?

        if (t > DELAY_MS) {
            origTicks = UINT64_MAX;
            break;
        }
    }

}

// Print claw
void print_claw(){
    printf("\x1b[%d;%dH%s", CLAW_ROW-1, CLAW_COL-1, CLAW_TOP);
    printf("\x1b[%d;%dH%s", CLAW_ROW, CLAW_COL, CLAW_MID);
    printf("\x1b[%d;%dH%s", CLAW_ROW+1, CLAW_COL-1, CLAW_BOT);
}

// Print prize if within grid
void print_prize(int curr_x, int curr_y, int px, int py){
    int diff_x, diff_y;

    diff_x = px - curr_x;
    diff_y = py - curr_y;
    if ((abs(diff_x) < ((GRID_LINES_ROWS-1)/2)) &&
        (abs(diff_y) < ((GRID_LINES_COLS-1)/2))) {
        // -1 since PRIZE_MID is 3 characters wide
        printf("\x1b[%d;%dH%s", CLAW_ROW-diff_x, CLAW_COL+diff_y-1, PRIZE_MID);
    }
}

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
    char keysNames[28][32] = {
        "A", "B", "X", "Y",
        "StickL", "StickR", "L", "R",
        "ZL", "ZR", "Plus", "Minus",
        "Left", "Up", "Right", "Down",
        "StickLLeft", "StickLUp", "StickLRight", "StickLDown",
        "StickRLeft", "StickRUp", "StickRRight", "StickRDown",
        "LeftSL", "LeftSR", "RightSL", "RightSR",
    };

    //u32 kDownOld = 0, kHeldOld = 0, kUpOld = 0; //In these variables there will be information about keys detected in the previous frame

    int button_pressed = 0;

    int i, x, y;
    int machine_num, total_machines;
    int ax, ay;
    int bx, by;
    int px, py;
    int a_press, b_press;
    int curr_x, curr_y;
    int old_x, old_y;
    int tokens, prizes, prize_caught;
    int scrolling_x, scrolling_y;
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
    // Original: 80 A presses, 40 B presses
    ax = 94;
    ay = 34;
    bx = 22;
    by = 67;
    px = 8400;
    py = 5400;
    // Modified: 11 A presses, 8 B presses
    a_press = 11;
    b_press = 8;
    ax = 17;
    ay = 9;
    bx = 12;
    by = 8;
    //ax = 5;//17;
    //ay = 3;//9;
    //bx = 4;//12;
    //by = 2;//8;
    px = a_press*ax + b_press*bx;//8400;
    py = a_press*ay + b_press*by;//5400;

    curr_x = 0;
    curr_y = 0;
    //old_i = -1;
    old_x = 0;
    old_y = 0;
    tokens = 0;
    prizes = 0;
    prize_caught = 0;
    scrolling_x = 0;
    scrolling_y = 0;
    grid_x_offset = 0;
    grid_y_offset = 0;

    printf("\x1b[1;1H Advent of Code 2024 Day 13: Claw Contraption");
    printf("\x1b[2;1H Instructions: Press A/B to move right/forward by some amount");
    printf("\x1b[3;1H               Press X/Y to move left/backward by the same amount,");
    printf("\x1b[4;1H                 but also costs tokens!");

    printf("\x1b[5;1H   Machine %d of %d", machine_num, total_machines);
    printf("\x1b[6;1H     Button A: X+%d, Y+%d", ax, ay);
    printf("\x1b[7;1H     Button B: X+%d, Y+%d", bx, by);
    printf("\x1b[8;1H     Prize: X=%d, Y=%d", px, py);

    printf("\x1b[10;1H   Current (X, Y) = (%d, %d)          ", curr_x, curr_y);
    printf("\x1b[11;1H   Tokens spent = %d", tokens);
    printf("\x1b[12;1H   Prizes caught = %d", prizes);
    printf("\x1b[13;1H   No button pressed yet");

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

        // Rewrite lines after clearing the whole screen
        printf("\x1b[1;1H Advent of Code 2024 Day 13: Claw Contraption");
        printf("\x1b[2;1H Instructions: Press A/B to move right/forward by some amount");
        printf("\x1b[3;1H               Press X/Y to move left/backward by the same amount,");
        printf("\x1b[4;1H                 but also costs tokens!");

        printf("\x1b[5;1H   Machine %d of %d", machine_num, total_machines);
        printf("\x1b[6;1H     Button A: X+%d, Y+%d", ax, ay);
        printf("\x1b[7;1H     Button B: X+%d, Y+%d", bx, by);
        printf("\x1b[8;1H     Prize: X=%d, Y=%d", px, py);

        printf("\x1b[10;1H   Current (X, Y) = (%d, %d)          ", curr_x, curr_y);
        printf("\x1b[11;1H   Tokens spent = %d", tokens);
        printf("\x1b[12;1H   Prizes caught = %d", prizes);
        
        // Check if some of the keys are down, held or up
        // Max index of 3 for A, B, X, Y
        button_pressed = 0;
        for (i = 0; i < 4; i++)
        {
            if (kDown & BIT(i)){
                //printf("%s down\n", keysNames[i]);

                //old_i = i;
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
                button_pressed = i+1;
                printf("\x1b[13;1H   Button %s pressed, position update: (%d, %d) -> (%d, %d)          ", keysNames[i], old_x, old_y, curr_x, curr_y);
                break;
            }
            //if (kHeld & BIT(i)) printf("%s held\n", keysNames[i]);
            //if (kUp & BIT(i)) printf("%s up\n", keysNames[i]);
        }
        //}

        // Check current position vs prize position
        if ((curr_x > px) || (curr_y > py)) {
            // Overshot and did not get the prize
            printf("\x1b[14;1H   Went beyond the prize! Go back with X/Y!");
            prize_caught = 0;
        }
        else if ((curr_x == px) && (curr_y == py)) {
            // Got the prize
            printf("\x1b[14;1H   Congratulations! You caught a prize!");
            if (!prize_caught) {
                prizes = prizes + 1;
                prize_caught = 1;
            }

            // TODO: Print option to go to next machine
        }
        else {
            prize_caught = 0;
        }

        // TODO: handle negative coordinates
        if (button_pressed) {

            // Print grid lines
            // TODO: Implement Bresenham's algorithm for straight line animation?
            // Horizontal scroll
            // Compute y offset only once since this is constant during horizontal scroll
            grid_y_offset = old_y % 10;
            for (x = 1; x < abs(curr_x - old_x)+1; x++){
                wait_delay();

                if (curr_x > old_x) {
                    // A/B button pressed and x will increase during scroll
                    scrolling_x = old_x + x;
                } else if (curr_x < old_x) {
                    // X/Y button pressed and x will decrease during scroll
                    scrolling_x = old_x - x;
                }

                // Print real time coordinates - still old_y here since vertical scroll hasn't started
                printf("\x1b[10;1H   Current (X, Y) = (%d, %d)          ", scrolling_x, old_y);
                grid_x_offset = scrolling_x % 10;

                for (i = 0 ; i < GRID_LINES_ROWS; i++) {
                    printf("\x1b[%d;%dH", INIT_ROW_GRID_LINES+i, INIT_COL_GRID_LINES);
                    snprintf(sliced_grid_line, GRID_LINES_COLS+1, "%s", grid_lines[ i + 10 - grid_y_offset] + grid_x_offset);
                    printf("%s", sliced_grid_line);
                }

                // Need to reprint claw, prize, and borders
                // Print claw
                print_claw();

                // Print prize if within grid
                print_prize(curr_x, curr_y, px, py);

                // Print borders
                print_borders();

                // Update the console, sending a new frame to the display
                consoleUpdate(NULL);
            }
            // Vertical scroll
            // Compute x offset only once since this is constant during horizontal scroll
            grid_x_offset = curr_x % 10;
            for (y = 1; y < abs(curr_y - old_y)+1; y++) {
                wait_delay();

                // x offset is constant, and already increased to the final value during horizontal scroll
                if (curr_y > old_y) {
                    // A/B button pressed and y will increase during scroll
                    scrolling_y = old_y + y;
                } else if (curr_y < old_y) {
                    // X/Y button pressed and y will decrease during scroll
                    scrolling_y = old_y - y;
                }

                // Print real time coordinates - already curr_x here since horizontal scroll is done
                printf("\x1b[10;1H   Current (X, Y) = (%d, %d)          ", curr_x, scrolling_y);
                grid_y_offset = scrolling_y % 10;

                for (i = 0 ; i < GRID_LINES_ROWS; i++) {
                    printf("\x1b[%d;%dH", INIT_ROW_GRID_LINES+i, INIT_COL_GRID_LINES);
                    snprintf(sliced_grid_line, GRID_LINES_COLS+1, "%s", grid_lines[ i + 10 - grid_y_offset] + grid_x_offset);
                    printf("%s", sliced_grid_line);
                }

                // Need to reprint claw, prize, and borders
                // Print claw
                print_claw();

                // Print prize if within grid
                print_prize(curr_x, curr_y, px, py);

                // Print borders
                print_borders();

                // Update the console, sending a new frame to the display
                consoleUpdate(NULL);
            }
        }
        else {
            grid_x_offset = curr_x % 10;
            grid_y_offset = curr_y % 10;

            // Still print grid lines when no button is pressed since the screen was cleared,
            // but print with no delay
            for (i = 0 ; i < GRID_LINES_ROWS; i++) {
                printf("\x1b[%d;%dH", INIT_ROW_GRID_LINES+i, INIT_COL_GRID_LINES);
                snprintf(sliced_grid_line, GRID_LINES_COLS+1, "%s", grid_lines[ i + 10 - grid_y_offset] + grid_x_offset);
                printf("%s", sliced_grid_line);
            }

            // Print claw
            print_claw();

            // Print prize if within grid
            print_prize(curr_x, curr_y, px, py);

            // Print borders
            print_borders();
        }

        // Set keys old values for the next frame
        //kDownOld = kDown;
        //kHeldOld = kHeld;
        //kUpOld = kUp;

        // Update the console, sending a new frame to the display
        consoleUpdate(NULL);
    }

    // Deinitialize and clean up resources used by the console (important!)
    consoleExit(NULL);
    return 0;
}
