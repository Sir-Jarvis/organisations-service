import pika, json, os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_institution.settings')
django.setup()

from offres.models import AnneeScolaire


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))#url du rabbit sur producer.py

channel = connection.channel()

channel.queue_declare(queue='accounts')#porte le mm nom sur le producer.C'est ce qui stocke les données


def callback(ch, method, properties, body):
    print('Received in documents')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'annee_created':
        annee_scolaire = AnneeScolaire(id=data['id'], date_debut=data['date_debut'],date_fin=data['date_fin'],alias=data['alias'])
        annee_scolaire.save()
        print('annee scolaire Created')

   
channel.basic_consume(queue='accounts', on_message_callback=callback, auto_ack=True)

print('Started Consuming') c

channel.start_consuming()


