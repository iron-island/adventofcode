// Include the most common headers from the C standard library
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Include the main libnx system header, for Switch development
#include <switch.h>

// See also libnx pad.h / hid.h.

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

    printf("\x1b[1;1H Advent of Code 2024 Day 13: Claw Contraption");
    printf("\x1b[2;1H Instructions: Press A/B to move right/forward");
    printf("\x1b[3;1H               Press X/Y to cancel A/B movements (no token refunds!)");

    int machine_num, total_machines;
    int ax, ay;
    int bx, by;
    int px, py;
    int curr_x, curr_y;
    int old_i, old_x, old_y;
    int tokens, prizes;

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
            int i;
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
            printf("\x1b[13;1H   Went beyond the prize! Go back!");
        }
        else if ((curr_x == px) && (curr_y == py)) {
            // Got the prize
            printf("\x1b[13;1H   Prize caught!");
            prizes = prizes + 1;

            // TODO: Print option to go to next machine
        }

        // Set keys old values for the next frame
        kDownOld = kDown;
        kHeldOld = kHeld;
        kUpOld = kUp;

        // Read the sticks' position
        //HidAnalogStickState analog_stick_l = padGetStickPos(&pad, 0);
        //HidAnalogStickState analog_stick_r = padGetStickPos(&pad, 1);

        // Print the sticks' position
        //printf("\x1b[3;1H%04d; %04d", analog_stick_l.x, analog_stick_l.y);
        //printf("\x1b[5;1H%04d; %04d", analog_stick_r.x, analog_stick_r.y);

        // Update the console, sending a new frame to the display
        consoleUpdate(NULL);
    }

    // Deinitialize and clean up resources used by the console (important!)
    consoleExit(NULL);
    return 0;
}
