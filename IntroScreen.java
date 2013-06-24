import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.awt.Color;
/**
 * Write a description of class IntroScreen here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class IntroScreen extends Screens
{
    private GreenfootImage introscreen;
    
    public IntroScreen()
    {
        introscreen = new GreenfootImage("introscreen.gif");
        setImage(introscreen);

    }

    public void act()
    {

        
        if(Greenfoot.mousePressed(this))
        {
            Grid grid = getGrid();
            grid.startGame();
        }
    }



}
