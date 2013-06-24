import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.util.List;
/**
 * Write a description of class Hero here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Hero extends Walkers
{
    private int turnCount = 0;
    private boolean alive;
    private int steps;
    private GreenfootImage deadHero;
    private GreenfootImage deadHero2;
    private GreenfootImage aliveHero;
    private GreenfootImage aliveHero2;

    public Hero()
    {
        alive = true;
        deadHero = new GreenfootImage("ZombieHero.gif");
        deadHero2 = new GreenfootImage("ZombieHero2.gif");
        aliveHero = new GreenfootImage("Hero.gif");
        aliveHero2 = new GreenfootImage("Hero2.gif");
        setImage(aliveHero);
    }

    public void act() 
    {

        turnCount++;
        animateHero();
        while(turnCount>10)
        {
            checkKeys();
            turnCount=0;

        }
        if(alive)
        {
            killHero(collideZombie());
        }
        keepScore();
    }  

    public void killHero(boolean eaten)
    {
        if(eaten)
        {   Grid grid = getGrid();
            if(getImage()==aliveHero||getImage()==aliveHero2)
            {
                Greenfoot.playSound("die.wav");
            }
            grid.endGame();
            setImage(deadHero);
            alive = false;
        }

    }

    public void animateHero()
    {
        if(alive)
        {
            animateActor(aliveHero,aliveHero2);
        }
        else
        {
            animateActor(deadHero,deadHero2);
        }
    }

    public void keepScore()
    {
        steps = getSteps();
        Grid grid = getGrid();
        List list = grid.getObjects(Steps.class);
        grid.removeObjects(list);
        grid.addObject(new Steps(steps),getX(),getY());
    }
}
