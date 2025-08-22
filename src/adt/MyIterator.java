package adt;

/**
 * Author: Your Name
 * A simple iterator interface for custom collections (no java.util.Iterator).
 */
public interface MyIterator<T> {
	boolean hasNext();
	T next();
}