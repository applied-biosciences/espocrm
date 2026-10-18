<?php
namespace Espo\Custom\Classes\RecordHooks\Account;

use Espo\Core\Record\Hook\UnlinkHook;
use Espo\ORM\Entity;
use Espo\ORM\EntityManager;

/** Removing a family member from its customer also removes it from that customer's booking. */
class UnlinkTravellerFromBooking implements UnlinkHook
{
    public function __construct(private EntityManager $entityManager)
    {}

    public function process(Entity $entity, string $link, Entity $foreignEntity): void
    {
        if ($link !== 'travellers' || $foreignEntity->getEntityType() !== 'NvTraveller') {
            return;
        }

        $bookingId = $foreignEntity->get('bookingId');

        if (!$bookingId) {
            return;
        }

        $booking = $this->entityManager->getEntityById('NvBooking', $bookingId);

        if (!$booking || $booking->get('customerId') !== $entity->getId()) {
            return;
        }

        $foreignEntity->set('bookingId', null);
        $this->entityManager->saveEntity($foreignEntity);

        if ($booking->get('leadTravellerId') === $foreignEntity->getId()) {
            $booking->set('leadTravellerId', null);
            $this->entityManager->saveEntity($booking);
        }
    }
}
