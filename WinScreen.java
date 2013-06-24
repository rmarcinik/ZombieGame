import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * Write a description of class WinScreen here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class WinScreen extends Screens
{
    private GreenfootImage winscreen;
    public WinScreen()
    {
        winscreen= new GreenfootImage("winscreen.gif");
        setImage(winscreen);
    }
public void act()
{
    if(Greenfoot.mousePressed(this))
    {
        Grid grid = getGrid();
        grid.removeObjects(grid.getObjects(null));
        grid.addObject(new IntroScreen(),10,10);
    }
}

}
