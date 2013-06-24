import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.awt.Color;
import java.awt.Font;
/**
 * Write a description of class Steps here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Steps extends Screens
{  
    private int width;
    private int height;
    private GreenfootImage scoreticker;
    private int score;
    public Steps()
    {
        this(0);
    }

    public Steps(int num)
    {
        score = num;
        updateImage();
    }
    public void updateImage()
    {
        scoreticker = new GreenfootImage(30,30);
        scoreticker.setColor(new Color(40,40,40,100));
        Font font = new Font("SansSerif",Font.PLAIN,9);
        scoreticker.setFont(font);
        scoreticker.drawString(""+score,19,28);
        setImage(scoreticker);
    }
 
}
