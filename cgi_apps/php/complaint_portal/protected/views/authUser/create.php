<?php
/* @var $this AuthUserController */
/* @var $model AuthUser */

$this->breadcrumbs=array(
	'Auth Users'=>array('index'),
	'Create',
);

$this->menu=array(
	array('label'=>'List AuthUser', 'url'=>array('index')),
	array('label'=>'Manage AuthUser', 'url'=>array('admin')),
);
?>

<h1>Create AuthUser</h1>

<?php $this->renderPartial('_form', array('model'=>$model)); ?>