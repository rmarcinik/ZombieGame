import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.util.List;
/**
 * Write a description of class ZombieParts here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class ZombiePile extends Walkers
{
    private GreenfootImage zombiepile;

    public ZombiePile()
    {
        zombiepile = new GreenfootImage("ZombiePile2.gif");
        setImage(zombiepile);
    }

    public void act() 
    {
        winCheck();
        removePile(collideZombie());

    }  

    public void removePile(boolean b)
    {
        if(b)
        {
            World world = getWorld();
            world.removeObject(this);
        }
    }

    public void winCheck()
    {
        Grid grid = getGrid();
        List zombies = grid.getObjects(Zombie.class);
        int z = zombies.size();
        
        if(z==0)
        {
            grid.winGame();
        }

    }
}
