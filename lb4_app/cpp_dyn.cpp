#include <iostream>

struct Node {
    int data;
    Node* prev;
    Node* next;
};

struct List {
    Node* head;
    Node* tail;
    int count;
};

extern "C" {
    // Создание списка
    List* create_list() {
        List* l = new List;
        l->head = nullptr;
        l->tail = nullptr;
        l->count = 0;
        return l;
    }

    // Очистка списка
    void clear_list(List* l) {
        Node* curr = l->head;
        while (curr != nullptr) {
            Node* temp = curr;
            curr = curr->next;
            delete temp;
        }
        l->head = nullptr;
        l->tail = nullptr;
        l->count = 0;
    }

    // Удаление самого объекта списка (для освобождения памяти)
    void destroy_list(List* l) {
        clear_list(l);
        delete l;
    }

    // Вставка в конец
    void push_back(List* l, int value) {
        Node* nw = new Node{value, l->tail, nullptr};
        if (l->tail) l->tail->next = nw;
        else l->head = nw;
        l->tail = nw;
        l->count++;
    }

    // Вставка в начало
    void push_front(List* l, int value) {
        Node* nw = new Node{value, nullptr, l->head};
        if (l->head) l->head->prev = nw;
        else l->tail = nw;
        l->head = nw;
        l->count++;
    }

    // Вставка по индексу (0-based)
    int insert_at(List* l, int index, int value) {
        if (index < 0 || index > l->count) return -1; // Ошибка
        if (index == 0) { push_front(l, value); return 0; }
        if (index == l->count) { push_back(l, value); return 0; }

        Node* nw = new Node{value, nullptr, nullptr};
        Node* curr = l->head;
        for (int i = 0; i < index - 1; ++i) curr = curr->next;
        
        nw->prev = curr;
        nw->next = curr->next;
        curr->next->prev = nw;
        curr->next = nw;
        l->count++;
        return 0;
    }

    // Удаление по индексу (0-based)
    int delete_at(List* l, int index) {
        if (l->count == 0 || index < 0 || index >= l->count) return -1;

        Node* target;
        if (index == 0) {
            target = l->head;
            l->head = l->head->next;
            if (l->head) l->head->prev = nullptr;
            else l->tail = nullptr;
        } else if (index == l->count - 1) {
            target = l->tail;
            l->tail = l->tail->prev;
            if (l->tail) l->tail->next = nullptr;
            else l->head = nullptr;
        } else {
            target = l->head;
            for (int i = 0; i < index; ++i) target = target->next;
            target->prev->next = target->next;
            target->next->prev = target->prev;
        }
        delete target;
        l->count--;
        return 0;
    }

    int get_count(List* l) { return l->count; }

    int get_element_at(List* l, int index) {
        if (index < 0 || index >= l->count) return -999999;
        Node* curr = l->head;
        for (int i = 0; i < index; ++i) curr = curr->next;
        return curr->data;
    }
}