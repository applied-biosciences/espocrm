<?php
require '/var/www/html/vendor/autoload.php';
$s3 = new AsyncAws\S3\S3Client([
    'endpoint'=>'http://minio:9000', 'region'=>'us-east-1','pathStyleEndpoint'=>true,
    'accessKeyId'=>getenv('MINIO_ACCESS_KEY'), 'accessKeySecret'=>getenv('MINIO_SECRET_KEY'),
]);
$bucket=getenv('MINIO_BUCKET');
$found=false;
foreach ($s3->listBuckets()->getBuckets() as $item) {
    if ($item->getName()===$bucket) {$found=true;}
}
if (!$found) {$s3->createBucket(['Bucket'=>$bucket])->resolve();}
echo "Private synthetic-document bucket ready.\n";
