<?php
namespace Espo\Custom\Core\FileStorage\Storages;

use Espo\Core\Exceptions\NotFound;
use Espo\Core\FileStorage\Attachment;
use Psr\Http\Message\StreamInterface;
use RuntimeException;

/** Preserve Espo's S3 adapter while returning 404 for stale, removed object links. */
class S3 extends \Espo\Core\FileStorage\Storages\AwsS3
{
    public function getStream(Attachment $attachment): StreamInterface
    {
        try {
            return parent::getStream($attachment);
        } catch (RuntimeException $error) {
            // Only translate a confirmed missing object; retain operational/storage errors.
            if (!parent::exists($attachment)) {
                throw new NotFound('Document file no longer exists.');
            }
            throw $error;
        }
    }
}
