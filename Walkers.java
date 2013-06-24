import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.util.List;
/**
 * Write a description of class Walkers here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Walkers extends Actor
{
    public int direction;
    private int stepstaken=0;
    private static boolean takeTurn=false;
    private static int turnCounter;
    private int count=0;
    

    public void act()
    {

    }

    public void moveOne(int dir)
    {
        if(dir == 1)
        {
            setLocation(getX(),getY()-1);
            stepstaken++;
        }
        if(dir == 2)
        {
            setLocation(getX()+1,getY()-1);
            stepstaken++;
        }
        if(dir == 3)
        {
            setLocation(getX()+1,getY());
            stepstaken++;
        }
        if(dir == 4)
        {
            setLocation(getX()+1,getY()+1);
            stepstaken++;
        }
        if(dir == 5)
        {
            setLocation(getX(),getY()+1);
            stepstaken++;
        }
        if(dir == 6)
        {
            setLocation(getX()-1,getY()+1);
            stepstaken++;
        }
        if(dir == 7)
        {
            setLocation(getX()-1,getY());
            stepstaken++;
        }
        if(dir == 8)
        {
            setLocation(getX()-1,getY()-1);
            stepstaken++;
        }

    }

    public void checkKeys()
    {
        if(Greenfoot.isKeyDown("left"))
        {
            moveOne(7);
            takeTurn=true;
        }
        if(Greenfoot.isKeyDown("right"))
        {
            moveOne(3);
            takeTurn=true;
        }
        if(Greenfoot.isKeyDown("up"))
        {
            moveOne(1);
            takeTurn=true;
        }
        if(Greenfoot.isKeyDown("down"))
        {
            moveOne(5);
            takeTurn=true;
        }
        if(Greenfoot.isKeyDown("space"))
        {
            setLocation(Greenfoot.getRandomNumber(20),Greenfoot.getRandomNumber(20));
            takeTurn=true;
        }

    }

    public boolean collideZombie()
    {
        Actor z = getOneIntersectingObject(Zombie.class);
        Actor p = getOneIntersectingObject(ZombiePile.class);
        if (z!=null || p!=null)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    public Grid getGrid()
    {
        return (Grid) getWorld();
    }
    
    public void animateActor(GreenfootImage first, GreenfootImage second)
    {   
        count++;
       
        if(getImage()== first && count>20)
        {
            setImage(second);
            count=0;
        }
        if(getImage()== second && count>20)
        {
            setImage(first);
            count=0;
        }
    }
    
    public boolean getTurn()
    {
        return takeTurn;
    }
    public void endTurn()
    {
        
        Grid grid = getGrid();
        List<Zombie> zlist = grid.getObjects(Zombie.class);
        int numberzombies = zlist.size();
        if(turnCounter>=numberzombies)
        {
            takeTurn=false;
            turnCounter=0;
        }
        turnCounter++;
        
    }
    public int getSteps()
    {
        return stepstaken;
    }
    
}
