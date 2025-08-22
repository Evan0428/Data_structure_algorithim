package adt;

/**
 * Author: Your Name
 * Singly linked list implementation of MyList ADT.
 */
public class SinglyLinkedList<T> implements MyList<T> {
	private static class Node<E> {
		E data;
		Node<E> next;
		Node(E data) { this.data = data; }
	}

	private Node<T> head;
	private Node<T> tail;
	private int size;

	@Override
	public int size() { return size; }

	@Override
	public boolean isEmpty() { return size == 0; }

	@Override
	public void clear() {
		head = null;
		tail = null;
		size = 0;
	}

	@Override
	public void addFirst(T element) {
		Node<T> node = new Node<>(element);
		node.next = head;
		head = node;
		if (tail == null) tail = node;
		size++;
	}

	@Override
	public void addLast(T element) {
		Node<T> node = new Node<>(element);
		if (tail == null) {
			head = tail = node;
		} else {
			tail.next = node;
			tail = node;
		}
		size++;
	}

	@Override
	public void add(int index, T element) {
		checkPositionIndex(index);
		if (index == 0) { addFirst(element); return; }
		if (index == size) { addLast(element); return; }
		Node<T> prev = nodeAt(index - 1);
		Node<T> node = new Node<>(element);
		node.next = prev.next;
		prev.next = node;
		size++;
	}

	@Override
	public T get(int index) {
		checkElementIndex(index);
		return nodeAt(index).data;
	}

	@Override
	public T set(int index, T element) {
		checkElementIndex(index);
		Node<T> n = nodeAt(index);
		T old = n.data;
		n.data = element;
		return old;
	}

	@Override
	public T removeFirst() {
		if (head == null) throw new IndexOutOfBoundsException("List is empty");
		T val = head.data;
		head = head.next;
		if (head == null) tail = null;
		size--;
		return val;
	}

	@Override
	public T removeAt(int index) {
		checkElementIndex(index);
		if (index == 0) return removeFirst();
		Node<T> prev = nodeAt(index - 1);
		Node<T> curr = prev.next;
		prev.next = curr.next;
		if (curr == tail) tail = prev;
		size--;
		return curr.data;
	}

	@Override
	public boolean contains(T element) {
		return indexOf(element) != -1;
	}

	@Override
	public int indexOf(T element) {
		int i = 0;
		for (Node<T> n = head; n != null; n = n.next) {
			if (element == null ? n.data == null : element.equals(n.data)) return i;
			i++;
		}
		return -1;
	}

	@Override
	public Object[] toArray() {
		Object[] arr = new Object[size];
		int i = 0;
		for (Node<T> n = head; n != null; n = n.next) arr[i++] = n.data;
		return arr;
	}

	@Override
	public MyIterator<T> iterator() {
		return new MyIterator<T>() {
			private Node<T> current = head;
			@Override public boolean hasNext() { return current != null; }
			@Override public T next() {
				T val = current.data;
				current = current.next;
				return val;
			}
		};
	}

	private Node<T> nodeAt(int index) {
		Node<T> n = head;
		for (int i = 0; i < index; i++) n = n.next;
		return n;
	}

	private void checkElementIndex(int index) {
		if (index < 0 || index >= size) throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
	}

	private void checkPositionIndex(int index) {
		if (index < 0 || index > size) throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
	}
}