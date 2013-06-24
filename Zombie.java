import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.util.List;
import java.util.ArrayList;
/**
 * Write a description of class Zombie here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Zombie extends Walkers
{
    private double deltaX;
    private double deltaY;
    private double absX;
    private double absY;
    private int direction;
    //Images
    private GreenfootImage zombie;
    private GreenfootImage zombie2;

    public Zombie()
    {

        zombie = new GreenfootImage("Zombie.gif");
        zombie2 = new GreenfootImage("Zombie2.gif");
        setImage(zombie);
    }

    public void act() 
    {

        animateActor(zombie,zombie2);
        if(getTurn()==true)
        {
            moveOne(direction);
            endTurn();
        }

        simplifyDirection();
        
        killZombie(collideZombie());
    }  

    /**
     * Gets the distance between Zombie and Hero
     */
    public void directionVectors(Actor target)
    {
        deltaX = (target.getX() - getX());
        deltaY = (target.getY() - getY());
    }

    /**
     * Takes the distance between Zombie and Hero 
     * and turns it into a North(1),NorthEast(2),East(3),SouthEast(4),South(5),
     * SouthWest(6),West(7),NorthWest(8) value
     */
    public void simplifyDirection()
    {
        Grid grid = getGrid();
        Hero h = grid.getHero();
        if(h != null)
        {
            directionVectors(h);

            if(deltaX<=0 && deltaY>=0)//above and right of Hero
            {
                absX = deltaX*(-1);
                if(absX==deltaY)
                {
                    direction =6;
                }
                else if(absX>deltaY)
                {
                    direction = 7;
                }
                else
                {
                    direction = 5;
                }

            }
            if(deltaX<=0 && deltaY<=0)//below and right of Hero
            {
                absX = deltaX*(-1);
                absY = deltaY*(-1);
                if(absX==absY)
                {
                    direction = 8;
                }
                else if(absX>absY)
                {
                    direction = 7;
                }
                else
                {
                    direction = 1;
                }

            }
            if(deltaX>=0 && deltaY<=0)//below and left of hero
            {
                absY = deltaY*(-1);
                if(deltaX==absY)
                {
                    direction = 2;
                }
                else if(deltaX>absY)
                {
                    direction = 3;
                }
                else
                {
                    direction = 1;
                }

            }
            if(deltaX>=0 && deltaY>=0)//above and left of hero
            {
                if(deltaX==deltaY)
                {
                    direction = 4;
                }
                else if(deltaX>deltaY)
                {
                    direction = 3;
                }
                else
                {
                    direction = 5;
                }

            }

        }
    }

    public void killZombie(boolean crashed)
    {
        if(crashed)
        {
            World world = getWorld();
            Greenfoot.playSound("die.wav");
            world.addObject(new ZombiePile(),getX(),getY());
            world.removeObject(this);
            
        }
    }

    public void smellHero()
    {
        List<Hero> hero = getObjectsInRange(1,Hero.class);
        if(hero != null)
        {
            Greenfoot.playSound("roar.wav");
        }
    }

}
