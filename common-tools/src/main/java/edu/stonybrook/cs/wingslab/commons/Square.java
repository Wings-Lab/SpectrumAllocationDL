package edu.stonybrook.cs.wingslab.commons;

/**
 * Square shape.
 * @author Mohammad Ghaderibaneh <mghaderibane@cs.stonybrook.edu>
 * @version 1.0
 * @since 1.0
 */
public class Square extends Rectangle{
    /**
     * Create Square object given side, originated in Point(0, 0)
     *
     * @param side square side
     */
    public Square(int side) {
        super(side, side);
    }

    /**Copy constructor
     * @param square Square object*/
    public Square(Square square){ super(square.getWidth(), square.getLength()); }

    @Override
    public String toString() {
        return "%1$s%2$s".formatted(Square.class.getSimpleName().toLowerCase(), this.getLength());
    }
}
