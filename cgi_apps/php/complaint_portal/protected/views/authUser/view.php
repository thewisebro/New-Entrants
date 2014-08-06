<?php
/* @var $this AuthUserController */
/* @var $model AuthUser */

$this->breadcrumbs=array(
	'Auth Users'=>array('index'),
	$model->id,
);

$this->menu=array(
	array('label'=>'List AuthUser', 'url'=>array('index')),
	array('label'=>'Create AuthUser', 'url'=>array('create')),
	array('label'=>'Update AuthUser', 'url'=>array('update', 'id'=>$model->id)),
	array('label'=>'Delete AuthUser', 'url'=>'#', 'linkOptions'=>array('submit'=>array('delete','id'=>$model->id),'confirm'=>'Are you sure you want to delete this item?')),
	array('label'=>'Manage AuthUser', 'url'=>array('admin')),
);
?>

<h1>View AuthUser #<?php echo $model->id; ?></h1>

<?php $this->widget('zii.widgets.CDetailView', array(
	'data'=>$model,
	'attributes'=>array(
		'id',
		'username',
		'first_name',
		'last_name',
		'email',
		'password',
		'is_staff',
		'is_active',
		'is_superuser',
		'last_login',
		'date_joined',
	),
)); ?>
