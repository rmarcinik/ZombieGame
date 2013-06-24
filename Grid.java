import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.awt.Color;
import java.util.List;
/**
 * Write a description of class Grid here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Grid extends World
{
    private Hero hero;
    private boolean win;
    /**
     * Constructor for objects of class Grid.
     * 
     */
    public Grid()
    {    
        super(20,20,30); 
        setPaintOrder(IntroScreen.class,Hero.class,Steps.class,WinScreen.class,GameOverScreen.class,
        Zombie.class,ZombiePile.class);
        setBackground("Cell.gif");
        setActOrder(Hero.class,Zombie.class,ZombiePile.class);
        addObject(new IntroScreen(),10,10);

    }

    public void makeZombies()
    {
        makeZombies(12);
    }

    public Hero getHero()
    {
        return hero;
    }

    public void startGame()
    {
        List all = getObjects(null);
        removeObjects(all);
        hero = new Hero();
        addObject(hero,9,9);
        makeZombies();
        win=false;
    }

    public void endGame()
    {
        if(win==false)
        {
            Greenfoot.playSound("lose.wav");
            addObject(new GameOverScreen(),9,8);
            win=true;
        }
    }

    public void winGame()
    {   
        if(win==false)
        {
            win=true;
            addObject(new WinScreen(),9,8);
            Greenfoot.playSound("win.wav");
        }
    }

    public void makeZombies(int number)
    {
        for(int i=0;i<number;i++)
        {
            addObject(new Zombie(),Greenfoot.getRandomNumber(20),Greenfoot.getRandomNumber(20)); 
        }
    }
}
