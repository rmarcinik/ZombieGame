import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.awt.Color;
/**
 * Write a description of class GameOverScreen here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class GameOverScreen extends Screens
{
    private GreenfootImage gameover;
   
    public GameOverScreen()
    {
        
        gameover = new GreenfootImage("gameover.png");
        setImage(gameover);
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
