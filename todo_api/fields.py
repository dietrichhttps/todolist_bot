from django.db import models
import time
import os
import threading

# Глобальный счетчик для обеспечения уникальности в рамках одного процесса
_counter = 0
_counter_lock = threading.Lock()

class CustomAutoField(models.BigAutoField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname, None):
            pk_value = self.generate_pk()
            setattr(model_instance, self.attname, pk_value)
            return pk_value
        else:
            return super().pre_save(model_instance, add)
    
    def generate_pk(self):
        global _counter
        # Получаем текущее время в наносекундах
        timestamp = time.time_ns()
        # Получаем ID процесса
        pid = os.getpid()
        # Получаем ID потока
        tid = threading.current_thread().ident
        # Увеличиваем счетчик атомарно
        with _counter_lock:
            _counter += 1
            counter = _counter
        
        # Собираем все компоненты в строку
        components = f"{timestamp}{pid}{tid}{counter}"
        # Преобразуем в число
        return int(components)