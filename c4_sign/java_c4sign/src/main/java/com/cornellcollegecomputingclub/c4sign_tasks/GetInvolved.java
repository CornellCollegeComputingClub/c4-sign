package com.cornellcollegecomputingclub.c4sign_tasks;

import com.cornellcollegecomputingclub.java_c4sign.JavaTaskBase;

import java.awt.image.BufferedImage;
import java.awt.image.WritableRaster;
import java.awt.Graphics2D;
import java.awt.Color;
import java.awt.Font;

/*
 * The intention of this class is to provide an animation that informs
 * students of how they can use the C4 Sign. It displays the following
 * text in sequence:
 *     Hey you!
 *     Do you want to put something on this sign?
 *     Scan this code!
 * 
 * It then displays a QR code pointing to the Github page.
 * Important: The QR code should be generated with python library Segno before use!
 * If the QR code has not been generated, the task should not run.
 * The QR code should point to http://github.com/CornellCollegeComputingClub/c4-sign
 * Note that the protocol has been changed to http instead of https.
 * This may not be good practice, but we need a shorter URL.
 * QR Code should not be micro, should use Version 3 at most, and use ECC level "L".
 * 
 * The text should flicker in a semi-animated style reminiscent of the video game
 * "Baba is You".
 */

public class GetInvolved extends JavaTaskBase {

    private int frame = 0;
    
    public GetInvolved () {
        super.setCanonicalName("GetInvolved");
        super.setTitle("Get involved!");
        super.setArtist("Mac Coleman");
        super.setDescription(
            "Will eventually display a message about how to contribute a task to the sign. Currently, it just displays the alphabet twice, once slowly, and then quickly."
        );

        frame = 0;
    }

    public boolean drawFrame(BufferedImage canvas, Graphics2D graphics, WritableRaster raster, double deltaTime) {

        String alphabets = "AAA BBB CCC DDD EEE FFF GGG HHH III JJJ KKK LLL MMM NNN OOO PPP QQQ RRR SSS TTT UUU VVV WWW XXX YYY ZZZ a b c d e f g h i j k l m n o p q r s t u v w x y z";
        frame += 1;
        frame %= alphabets.length();
        graphics.setColor(Color.WHITE);
        graphics.setFont(new Font("Arial", 0, 40));
        graphics.drawString(String.valueOf(alphabets.charAt(frame)), 0, 31);
        return false;
    }
}
