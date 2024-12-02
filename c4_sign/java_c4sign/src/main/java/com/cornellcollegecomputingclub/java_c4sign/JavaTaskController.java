package com.cornellcollegecomputingclub.java_c4sign;

import com.cornellcollegecomputingclub.c4sign_tasks.RainbowWaveJava;
import com.cornellcollegecomputingclub.c4sign_tasks.MemoryStress;
/* ------------------------------------------------------------
 * Import your java tasks here, at the end of the list above!!!
 * ------------------------------------------------------------
 */

import java.util.ArrayList;
import com.cornellcollegecomputingclub.java_c4sign.JavaTaskBase;

public class JavaTaskController {
    public static ArrayList<JavaTaskBase> getActiveTasks() {
        JavaTaskBase[] all_tasks = {
            new RainbowWaveJava(),
            new MemoryStress(),
            //Instantiate your java tasks here!
        };

        ArrayList<JavaTaskBase> runnable_tasks = new ArrayList<JavaTaskBase>();

        for (JavaTaskBase task : all_tasks) {
            if (!task.ignore) {
                runnable_tasks.add(task);
            }
        }

        return runnable_tasks;
    }

    public JavaTaskController() {
        System.out.println("JavaTaskController instantiated!");

        ArrayList<JavaTaskBase> available_tasks = getActiveTasks();

        System.out.println("Available tasks:");
        for (JavaTaskBase task : available_tasks) {
            System.out.println(task.toString());
        }
    }
}
