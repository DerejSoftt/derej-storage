from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from arrozcascara.models import Representante, Factura
from datetime import date, timedelta
from random import choice, randint, uniform
from decimal import Decimal


class Command(BaseCommand):
    help = "Carga datos de prueba en la base de datos"

    def handle(self, *args, **options):
        self.stdout.write("Cargando datos de prueba...")

        self._create_users()
        self._create_representantes()
        self._create_facturas()

        self.stdout.write(self.style.SUCCESS("Datos de prueba cargados exitosamente"))

    def _create_users(self):
        if not User.objects.filter(username="pope").exists():
            User.objects.create_superuser("pope", "admin@arrocera.com", "pope")
            self.stdout.write("  Usuario 'pope' creado")
        else:
            self.stdout.write("  Usuario 'pope' ya existe")

    def _create_representantes(self):
        if Representante.objects.exists():
            self.stdout.write("  Representantes ya existen, saltando...")
            return

        representantes = [
            ("V-12345678", "Carlos José Martínez"),
            ("V-23456789", "María Elena Rodríguez"),
            ("V-34567890", "Pedro Luis González"),
            ("V-45678901", "Ana Cecilia Fernández"),
            ("V-56789012", "José Gregorio Pérez"),
            ("V-67890123", "Rosa Amelia López"),
            ("V-78901234", "Luis Alberto Sánchez"),
            ("V-89012345", "Carmen Virginia Castillo"),
            ("V-90123456", "Jorge Enrique Medina"),
            ("V-10123456", "Sofía Beatriz Rivas"),
        ]

        for cedula, nombre in representantes:
            Representante.objects.create(
                cedula=cedula,
                nombre_completo=nombre,
                direccion=f"Dirección de {nombre.split()[-1]}"
            )

        self.stdout.write(f"  {len(representantes)} representantes creados")

    def _create_facturas(self):
        if Factura.objects.exists():
            self.stdout.write("  Facturas ya existen, saltando...")
            return

        representantes = list(Representante.objects.all())
        variedades = ["Puita", "Jaragua", "Guri", "Sabina", "Robusta"]
        nombres_clientes = [
            "Inversiones Agrícolas C.A.", "Molino Oriente S.A.",
            "Comercializadora Arrocera", "Distribuidora El Granero",
            "Agroindustria Los Llanos", "Procesadora de Arroz C.A.",
            "Empaques Agrícolas S.A.", "Exportadora RiceVenezuela",
            "Alimentos Polar", "Distribuidora Nacional",
            "Supermercado Central", "Abasto Los Jardines",
            "Mercado Mayorista", "Cooperativa Agrícola",
            "Industrias Alimenticias"
        ]

        today = date.today()
        facturas_creadas = 0

        for i in range(60):
            representante = choice(representantes)
            cliente = choice(nombres_clientes)
            variedad = choice(variedades)
            dias_atras = randint(1, 365)
            fecha = today - timedelta(days=dias_atras)
            cantidad_sacos = randint(10, 500)
            estado = choice(["pendiente", "pagado", "pendiente", "pendiente"])

            factura = Factura(
                numero_factura=f"FAC-{fecha.year}-{i+1:04d}",
                cedula=f"V-{randint(1000000, 25000000)}",
                nombre_cliente=cliente,
                cantidad_sacos=cantidad_sacos,
                representante=representante,
                fecha=fecha,
                variedad=variedad,
                estado=estado,
            )

            if estado == "pagado":
                factura.monto = Decimal(str(round(uniform(5000, 50000), 2)))
                factura.fecha_pago = fecha + timedelta(days=randint(1, 30))

            factura.save()
            facturas_creadas += 1

        self.stdout.write(f"  {facturas_creadas} facturas creadas")
