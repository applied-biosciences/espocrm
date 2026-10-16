<?php
/** Read-only local smoke evidence; not exposed over HTTP. */
chdir('/var/www/html');require 'bootstrap.php';
$app=new Espo\Core\Application();$c=$app->getContainer();
$app->getInjectableFactory()->create(Espo\Core\ApplicationUser::class)->setupSystemUser();
$em=$c->get('entityManager');
if ($argv[1]==='object') {
    $conf=$c->get('config');$a=$conf->get('awsS3Storage');
    $s3=new AsyncAws\S3\S3Client(['endpoint'=>$a['endpoint'],'region'=>$a['region'],'pathStyleEndpoint'=>true,
        'accessKeyId'=>$a['credentials']['key'],'accessKeySecret'=>$a['credentials']['secret']]);
    $keys=[];
    foreach ($s3->listObjectsV2(['Bucket'=>$a['bucketName']])->getContents() as $object) {$keys[]=$object->getKey();}
    echo json_encode(['exists'=>in_array($argv[2],$keys)])."\n";
} elseif ($argv[1]==='jobs') {
    $jobs=[];
    foreach ($em->getRDBRepository('ScheduledJob')->find() as $job) {
        $jobs[]=['name'=>$job->get('name'),'status'=>$job->get('status'),'lastRun'=>$job->get('lastRun')];
    }
    echo json_encode($jobs)."\n";
}
