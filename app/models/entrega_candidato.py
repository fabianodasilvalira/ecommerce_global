from sqlalchemy import Column, Integer, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum  # Import necessário

class EntregaCandidato(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceita', 'Aceita'),
        ('recusada', 'Recusada'),
    ]

    entrega = models.ForeignKey('Entrega', on_delete=models.CASCADE, related_name='candidatos')
    entregador = models.ForeignKey('Entregador', on_delete=models.CASCADE, related_name='entregas_candidatadas')
    data_interesse = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f'{self.entregador} → {self.entrega} ({self.status})'

