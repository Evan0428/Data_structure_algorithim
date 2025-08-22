package adt;

/**
 * Author: Your Name
 * Custom generic list ADT. Do not use Java Collections Framework.
 */
public interface MyList<T> {
	int size();
	boolean isEmpty();
	void clear();

	void addFirst(T element);
	void addLast(T element);
	void add(int index, T element);

	T get(int index);
	T set(int index, T element);
	T removeFirst();
	T removeAt(int index);

	boolean contains(T element);
	int indexOf(T element);

	Object[] toArray();

	MyIterator<T> iterator();
}