<?php
/** Idempotent local schema-v1 bootstrap. Secrets come only from the container environment. */
chdir('/var/www/html');
require_once 'bootstrap.php';
set_exception_handler(function (Throwable $error) {
    fwrite(STDERR, get_class($error) . ': ' . $error->getMessage() . PHP_EOL);
    exit(1);
});
$app = new Espo\Core\Application();
$c = $app->getContainer();
$app->getInjectableFactory()->create(Espo\Core\ApplicationUser::class)->setupSystemUser();
$em = $c->get('entityManager');
$config = $c->get('config');
$writer = $app->getInjectableFactory()->create(Espo\Core\Utils\Config\ConfigWriter::class);
if (getenv('SMTP_HOST') !== 'mailpit' || (int)getenv('SMTP_PORT') !== 1025) {
    throw new RuntimeException('Local Stage 3 email must use Mailpit (SMTP_HOST=mailpit, SMTP_PORT=1025).');
}
$model = json_decode(file_get_contents('/opt/nurivoyage/model.json'), true, 512, JSON_THROW_ON_ERROR);
if ($config->get('version') !== $model['espoVersion']) {
    throw new RuntimeException('EspoCRM version mismatch; do not silently upgrade.');
}
$tabs = array_merge(['Account', 'Contact', 'Lead'], $model['entities'], ['Email', 'Task', 'Document', 'EmailTemplate']);
$navigation = json_decode(file_get_contents('/opt/nurivoyage/navigation.json'), false, 512, JSON_THROW_ON_ERROR);
foreach ([
    'siteUrl' => getenv('APP_URL'), 'webSocketUrl' => getenv('WS_URL') ?: 'ws://localhost:8081',
    'theme'=>'NuriVoyage','themeParams'=>(object)['navbar'=>'side','direction'=>'ltr'],
    'userThemesDisabled'=>true,'loginView'=>'custom:views/nurivoyage/login',
    'logoSrc'=>'client/custom/branding/utnt-logo.png',
    'applicationDescription'=>"NuriVoyage — Travel Management Platform for Nuri's Travel",
    'applicationName' => 'NuriVoyage', 'companyName' => "Nuri's Travel",
    'defaultCurrency' => getenv('DEFAULT_CURRENCY'), 'baseCurrency' => getenv('DEFAULT_CURRENCY'),
    'currencyList' => ['ZAR','USD','GBP','EUR','SAR','AED'],
    // Synthetic illustrative rates only: finance must never use these as live rates.
    'currencyRates' => ['ZAR'=>1, 'USD'=>0.055, 'GBP'=>0.043, 'EUR'=>0.051, 'SAR'=>0.206, 'AED'=>0.202],
    'dateFormat' => 'DD/MM/YYYY', 'timeZone' => getenv('APP_TIMEZONE'),
    'tabList' => $navigation, 'quickCreateList' => ['Account','Contact','NvEnquiry','NvBooking','NvTravelDocument'],
    'smtpServer' => getenv('SMTP_HOST'), 'smtpPort' => (int) getenv('SMTP_PORT'),
    'smtpAuth' => false, 'smtpSecurity' => null, 'outboundEmailIsShared' => true,
    'outboundEmailFromName' => "NuriVoyage · Nuri's Travel (LOCAL)", 'outboundEmailFromAddress' => 'admin@nuri.local',
    'defaultFileStorage' => 'AwsS3', 'attachmentAvailableStorageList' => ['AwsS3'],
    'awsS3Storage' => [
        'bucketName' => getenv('MINIO_BUCKET'), 'path' => '', 'region' => 'us-east-1',
        'endpoint' => 'http://minio:9000', 'pathStyleEndpoint' => true, 'sendChunkedBody' => false,
        'credentials' => ['key'=>getenv('MINIO_ACCESS_KEY'), 'secret'=>getenv('MINIO_SECRET_KEY')],
    ],
    'nurivoyageSchemaVersion' => 1, 'fxProvider' => 'Frankfurter', 'fxProviderUrl' => 'https://api.frankfurter.app',
] as $key=>$value) { $writer->set($key,$value); }
$writer->save();
// Stage 11 migration: the Agents entity is a first-class Espo record backed by nv_agent.
// Keep this idempotent so local bootstrap can safely be rerun after a fresh volume restore.
$em->getSqlExecutor()->execute("CREATE TABLE IF NOT EXISTS nv_agent (
    id VARCHAR(24) NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    deleted TINYINT(1) DEFAULT 0,
    created_at DATETIME NULL,
    modified_at DATETIME NULL,
    user_id VARCHAR(24) NULL,
    assigned_user_id VARCHAR(24) NULL,
    created_by_id VARCHAR(24) NULL,
    modified_by_id VARCHAR(24) NULL,
    login VARCHAR(255) NULL,
    last_login_at DATETIME NULL,
    login_audit_trail TEXT NULL,
    completed_sales INT DEFAULT 0,
    open_sales INT DEFAULT 0,
    commission_type VARCHAR(100) NULL,
    commission_rate DECIMAL(16,8) NULL,
    commission_paid DECIMAL(16,8) DEFAULT 0,
    commission_paid_currency VARCHAR(3) NULL,
    commission_owed DECIMAL(16,8) DEFAULT 0,
    commission_owed_currency VARCHAR(3) NULL,
    description TEXT NULL,
    INDEX idx_nv_agent_name_deleted (name, deleted),
    INDEX idx_nv_agent_login_deleted (login, deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");
$em->getSqlExecutor()->execute("CREATE TABLE IF NOT EXISTS nv_agent_login (id VARCHAR(24) NOT NULL PRIMARY KEY, name VARCHAR(255) NOT NULL, deleted TINYINT(1) DEFAULT 0, created_at DATETIME NULL, modified_at DATETIME NULL, agent_id VARCHAR(24) NULL, event_type VARCHAR(20) NULL, event_at DATETIME NULL, ip_address VARCHAR(64) NULL, user_agent VARCHAR(255) NULL, description TEXT NULL, INDEX idx_nv_agent_login_agent (agent_id, deleted), INDEX idx_nv_agent_login_event (event_at)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");
// Repair tables previously created with the MariaDB server default collation.
foreach (['nv_agent', 'nv_agent_login'] as $table) {
    $em->getSqlExecutor()->execute("ALTER TABLE $table CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
}
function upsert(string $type, string $key, string $value, array $data) {
    global $em;
    $record = $em->getRDBRepository($type)->where([$key=>$value])->findOne();
    if (!$record) { $record = $em->getNewEntity($type); }
    $record->set(array_merge([$key=>$value],$data));
    $em->saveEntity($record);
    return $record;
}
// EspoCRM 10 resolves system SMTP from a Group Email Account matching the sender.
upsert('InboundEmail','emailAddress','admin@nuri.local',[
    'name'=>'NuriVoyage Local Mailpit','status'=>'Active','useImap'=>false,'useSmtp'=>true,
    'smtpIsShared'=>true,'smtpIsForMassEmail'=>false,'smtpHost'=>getenv('SMTP_HOST'),
    'smtpPort'=>(int)getenv('SMTP_PORT'),'smtpAuth'=>false,'smtpSecurity'=>'',
    'storeSentEmails'=>false,
]);
$common = ['Account','Contact','Lead','NvEnquiry','NvQuote','NvBooking','NvBookingItem','NvTraveller','NvCustomerInvoice','NvCustomerPayment','NvPackage','NvProduct','Email','Task'];
$ops = ['Account','Contact','NvBooking','NvBookingItem','NvTraveller','NvItinerarySegment','NvTravelDocument','NvHotel','NvFlight','NvTransfer','NvSightseeing','NvVisa','NvSupplier','NvPackage','NvProduct','Document','Email','Task'];
$finance = ['Account','Contact','NvBooking','NvBookingItem','NvTraveller','NvSupplier','NvPurchaseOrder','NvSupplierBill','NvCustomerInvoice','NvCustomerPayment','NvSupplierPayment','NvFxRate','NvCommission','NvAgent','Email','Task'];
$roles = [
    'Sales Agent' => $common,
    'Operations' => $ops,
    'Sales + Operations Hybrid' => array_unique(array_merge($common,$ops)),
    'Sales + Operations Commercial' => array_unique(array_merge($common,$ops,['NvPurchaseOrder','NvSupplierBill','NvAgent'])),
    'Finance' => $finance,
    'Management' => $tabs,
    'System Administrator' => [],
];
$roleIds=[];
$scopes = $c->get('metadata')->get(['scopes']);
foreach ($roles as $name=>$allowed) {
    // PDF generation uses the Template scope; all local operational roles need read access to select layouts.
    $allowed[] = "Template";
    $allowed[] = "NvPerformanceReport";
    $allowed[] = "NvCommunication";
    $allowed[] = "NvTaxRule";
    $allowed[] = "NvConversionSnapshot";
    $allowed[] = "NvWorkflowTask";
    $data=[]; $fields=[];
    // Default deny every ACL scope, including native reports/import/export surfaces.
    foreach ($scopes as $scope=>$def) {
        if ($c->get('metadata')->get(['scopes',$scope,'acl'])) { $data[$scope]=false; }
    }
    foreach ($allowed as $scope) {
        $data[$scope]=['create'=>'yes','read'=>'all','edit'=>'all','delete'=>'no','stream'=>'no'];
    }
    if ($name==='Operations') {
        foreach (['Account','Contact'] as $reference) {
            $data[$reference]=['create'=>'no','read'=>'all','edit'=>'no','delete'=>'no','stream'=>'no'];
        }
    }
    $data['User']=['create'=>'no','read'=>in_array($name,['Management','Finance'])?'all':'own','edit'=>'no','delete'=>'no','stream'=>'no'];
    if (in_array($name,['Sales Agent','Sales + Operations Hybrid','Sales + Operations Commercial'])) {
        $data['NvCommission']=['create'=>'no','read'=>'own','edit'=>'no','delete'=>'no','stream'=>'no'];
    }
    if (in_array($name,['Sales Agent','Operations','Sales + Operations Hybrid'])) {
        $fields['NvBookingItem']=array_fill_keys(['purchaseCost','purchaseCostCurrency','purchaseCostConverted'], ['read'=>'no','edit'=>'no']);
    }
    // Finance can see payment status and amount, but cannot rewrite commission ownership/rules.
    if ($name==='Finance') {
        $data['NvCommission']=['create'=>'no','read'=>'all','edit'=>'all','delete'=>'no','stream'=>'no'];
        $fields['NvCommission'] = array_fill_keys(['amount','method','ruleSnapshot','assignedUser','booking'], ['read'=>'yes','edit'=>'no']);
    }
    $role=upsert('Role','name',$name,[
        'data'=>(object)$data,'fieldData'=>json_decode(json_encode($fields ?: (object)[])),
        'exportPermission'=>'no','massUpdatePermission'=>'no','assignmentPermission'=>$name==='Management'?'all':'no',
        'userPermission'=>'no','portalPermission'=>'no','groupEmailAccountPermission'=>'no',
    ]);
    $roleIds[$name]=$role->getId();
}
$users=[
    'admin'=>'System Administrator','manager'=>'Management','finance'=>'Finance',
    'sales'=>'Sales Agent','operations'=>'Operations','hybrid'=>'Sales + Operations Hybrid',
    'hybrid-commercial'=>'Sales + Operations Commercial',
];
$userIds=[];
$hasher=$c->get('passwordHash');
foreach ($users as $login=>$roleName) {
    $username=$login.'@nuri.local';
    $existing=$em->getRDBRepository('User')->where(['userName'=>$username])->findOne();
    $values=['firstName'=>ucfirst($login),'lastName'=>'Demo','emailAddress'=>$username,'isActive'=>true,
        'type'=>$login==='admin'?'admin':'regular'];
    if (!$existing || in_array('--reset-passwords',$argv)) {
        $values['password']=$hasher->hash(getenv('DEV_USER_PASSWORD'));
    }
    $user=upsert('User','userName',$username,$values);
    foreach ($em->getRDBRepository('User')->getRelation($user,'roles')->find() as $oldRole) {
        $em->getRDBRepository('User')->getRelation($user,'roles')->unrelate($oldRole);
    }
    $em->getRDBRepository('User')->getRelation($user,'roles')->relateById($roleIds[$roleName]);
    $userIds[$login]=$user->getId();
}
// Seed two synthetic agent profiles and link them to the local demo logins.
$agentUsers = ['sales'=>'Aisha Khan','hybrid-commercial'=>'Omar Patel'];
foreach ($agentUsers as $login=>$agentName) {
    $agent=upsert('NvAgent','login',$login.'@nuri.local',['name'=>$agentName,'userId'=>$userIds[$login],'commissionType'=>'Percent of Sale','commissionRate'=>5,'description'=>'SYNTHETIC LOCAL AGENT PROFILE']);
    upsert('NvAgentLogin','name',$agentName.' Login',['agentId'=>$agent->getId(),'eventType'=>'Login','eventAt'=>'2026-10-17 08:30:00','ipAddress'=>'127.0.0.1','userAgent'=>'Synthetic UAT']);
    upsert('NvAgentLogin','name',$agentName.' Logout',['agentId'=>$agent->getId(),'eventType'=>'Logout','eventAt'=>'2026-10-17 17:00:00','ipAddress'=>'127.0.0.1','userAgent'=>'Synthetic UAT']);
}
// Role-safe synthetic Stage 13 management reports. Access is controlled by the role ACL above.
foreach ([
 ['Profitability','Profitability Dashboard',40000,25000,15000,0,0,0,0,2,1],
 ['Sales Performance','Sales Performance Dashboard',40000,0,0,0,0,0,0,2,1],
 ['Operations Performance','Operations Performance Dashboard',0,0,0,0,0,0,0,2,1],
 ['Supplier Payables','Supplier Payables Dashboard',0,0,0,0,12000,12000,12000,2,0],
 ['Debtors','Debtor Dashboard',40000,0,0,18000,0,0,0,2,1],
 ['Creditors','Creditor Dashboard',0,0,0,0,12000,12000,12000,2,0]
] as $r) { upsert('NvPerformanceReport','name',$r[1],['reportType'=>$r[0],'periodStart'=>'2026-10-01','periodEnd'=>'2026-10-31','salesTotal'=>$r[2],'costTotal'=>$r[3],'profitTotal'=>$r[4],'debtorTotal'=>$r[5],'creditorTotal'=>$r[6],'supplierOutstanding'=>$r[7],'openBookings'=>$r[8],'completedSales'=>$r[9],'description'=>'SYNTHETIC LOCAL STAGE 13 REPORT']); }
// Seed one synthetic task per Stage 16 automation class for local UAT.
foreach ([['Approval','Synthetic quote approval'],['Reminder','Synthetic customer reminder'],['Document Expiry','Synthetic passport expiry alert'],['Supplier Follow-up','Synthetic supplier confirmation follow-up'],['Exception','Synthetic unresolved exception']] as [$type,$name]) {
    upsert('NvWorkflowTask','name',$name,['workflowType'=>$type,'status'=>'Open','priority'=>$type==='Exception'?'High':'Normal','dueAt'=>'2026-10-31 09:00:00','reminderAt'=>'2026-10-24 09:00:00','lastAction'=>'Seeded Stage 16 synthetic workflow']);
}
// Seed only once. Re-running bootstrap preserves human UAT edits and transactions.
if (!$config->get('nurivoyageSeedVersion')) {
    $customers=[];
    foreach (['Ahmed Khan','Fatima Patel','Mohammed Ismail'] as $person) {
        $account=upsert('Account','name',$person,['assignedUserId'=>$userIds['sales'],'description'=>'SYNTHETIC LOCAL TEST CUSTOMER']);
        $customers[]=$account->getId();
        [$first,$last]=explode(' ',$person,2);
        upsert('Contact','lastName',$last,['firstName'=>$first,'accountId'=>$account->getId(),'assignedUserId'=>$userIds['sales']]);
    }
    $supplierIds=[];
    foreach (['Demo Airways','Demo Makkah Hotel','Demo Madinah Hotel','Demo Transfers','Demo Visa Services'] as $name) {
        $supplierIds[]=upsert('NvSupplier','name',$name,['emailAddress'=>'supplier@nuri.local'])->getId();
    }
    foreach (['Umrah Family Package','Dubai Holiday','Cape Town → London flight'] as $i=>$scenario) {
        $package=upsert('NvPackage','name',$scenario,['sellingPrice'=>40000+$i*5000,'sellingPriceCurrency'=>'ZAR']);
        $enquiry=upsert('NvEnquiry','name',$scenario,['customerId'=>$customers[$i],'status'=>'Qualified','assignedUserId'=>$userIds['sales']]);
        $booking=upsert('NvBooking','name',$scenario,['customerId'=>$customers[$i],'enquiryId'=>$enquiry->getId(),'packageId'=>$package->getId(),
            'status'=>'Booking Confirmed','supplierStatus'=>'Supplier Selected','sellingPrice'=>40000+$i*5000,'sellingPriceCurrency'=>'ZAR','assignedUserId'=>$userIds['sales']]);
        upsert('NvQuote','name',$scenario.' Quote',['bookingId'=>$booking->getId(),'enquiryId'=>$enquiry->getId(),'customerId'=>$customers[$i],
            'status'=>'Accepted','sellingPrice'=>40000+$i*5000,'sellingPriceCurrency'=>'ZAR','assignedUserId'=>$userIds['sales']]);
        foreach ([['Flight','USD',700],['Hotel','USD',400],['Transfer','SAR',500]] as $j=>[$type,$currency,$amount]) {
            upsert('NvBookingItem','name',$scenario.' '.$type,['bookingId'=>$booking->getId(),'supplierId'=>$supplierIds[[0,1,3][$j]],
                'productType'=>$type,'purchaseCost'=>$amount,'purchaseCostCurrency'=>$currency,'sellingPrice'=>10000,'sellingPriceCurrency'=>'ZAR']);
        }
        upsert('NvTraveller','name',['Ahmed Khan','Fatima Patel','Mohammed Ismail'][$i],['customerId'=>$customers[$i],'bookingId'=>$booking->getId()]);
        upsert('NvCustomerInvoice','name',$scenario.' Invoice',['bookingId'=>$booking->getId(),'customerId'=>$customers[$i],'amount'=>40000+$i*5000,'amountCurrency'=>'ZAR','status'=>'Issued']);
        upsert('NvCommission','name',$scenario.' Commission',['bookingId'=>$booking->getId(),'amount'=>500,'amountCurrency'=>'ZAR','method'=>'Fixed','assignedUserId'=>$userIds['sales'],'agentId'=>$em->getRDBRepository('NvAgent')->where(['login'=>'sales@nuri.local'])->findOne()->getId(),
            'ruleSnapshot'=>'Synthetic baseline only; immutable ledger and calculations are future scope.']);
        upsert('NvPurchaseOrder','name',$scenario.' PO',['bookingId'=>$booking->getId(),'supplierId'=>$supplierIds[0],'amount'=>700,'amountCurrency'=>'USD']);
    }
    // A different agent's commission is a negative security fixture.
    upsert('NvCommission','name','Other agent commission',['amount'=>123,'amountCurrency'=>'ZAR','assignedUserId'=>$userIds['hybrid']]);
    upsert('NvFxRate','name','SYNTHETIC USD/ZAR',['fromCurrency'=>'USD','toCurrency'=>'ZAR','rate'=>18.18,'rateDate'=>'2026-10-16']);
    $writer->set('nurivoyageSeedVersion',1);$writer->save();
}
echo "NuriVoyage schema v1 configured; seven roles/eight local logins; synthetic seed ready.\n";

foreach (['quotation','invoice','purchase-order'] as $kind) {
    $html=file_get_contents('/opt/nurivoyage/branding-email/'.$kind.'.html');
    $html=str_replace('[[APP_URL]]',rtrim(getenv('APP_URL'),'/'),$html);
    upsert('EmailTemplate','name','NuriVoyage — '.ucwords(str_replace('-',' ',$kind)),[
        'subject'=>'NuriVoyage | '.ucwords(str_replace('-',' ',$kind)),
        'body'=>$html,'isHtml'=>true,'status'=>'Active',
        'description'=>'Stage 3 branding foundation. Fill clearly marked placeholders with synthetic data before local testing. Mailpit only.',
    ]);
}
echo "Stage 3 theme, navigation and three branded email templates configured.\n";
// PDF templates are required by Espo's Print PDF action; keep one active local template per document type.
foreach ([
    'NvTravelDocument'=>'NuriVoyage Travel Document PDF', 'NvQuote'=>'NuriVoyage Quote PDF',
    'NvCustomerInvoice'=>'NuriVoyage Customer Invoice PDF', 'NvPurchaseOrder'=>'NuriVoyage Purchase Order PDF'
] as $entity=>$templateName) {
    upsert('Template','name',$templateName,['entityType'=>$entity,'status'=>'Active',
        'body'=>'<h1>{{name}}</h1><p><strong>Record ID:</strong> {{id}}</p><p><strong>Status:</strong> {{status}}</p><p><strong>Description:</strong> {{description}}</p>',
        'printHeader'=>false,'printFooter'=>true,'footer'=>'NuriVoyage · Local PDF']);
}

