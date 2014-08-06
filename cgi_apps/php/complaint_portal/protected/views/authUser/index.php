<?php
/* @var $this AuthUserController */
/* @var $dataProvider CActiveDataProvider */

$this->breadcrumbs=array(
	'Auth Users',
);

$this->menu=array(
	array('label'=>'Create AuthUser', 'url'=>array('create')),
	array('label'=>'Manage AuthUser', 'url'=>array('admin')),
);
?>

<h1>Auth Users</h1>

<?php $this->widget('zii.widgets.CListView', array(
	'dataProvider'=>$dataProvider,
	'itemView'=>'_view',
)); ?>
