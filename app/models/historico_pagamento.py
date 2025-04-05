import enum
from sqlalchemy import Column, Integer, DECIMAL, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app import models
from app.db.database import Base

class StatusPagamento(enum.Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    CANCELADO = "CANCELADO"

class HistoricoPagamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('autorizado', 'Autorizado'),
        ('falhou', 'Falhou'),
    ]

    pagamento = models.ForeignKey('Pagamento', on_delete=models.CASCADE, related_name='historicos')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente')
    metodo_pagamento = models.CharField(max_length=50)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pagamento} - {self.status} em {self.data.strftime("%d/%m/%Y %H:%M")}'
