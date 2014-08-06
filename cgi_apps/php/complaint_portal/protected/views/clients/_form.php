<?php
/* @var $this ClientsController */
/* @var $model Clients */
/* @var $form CActiveForm */
?>

<div class="form">

<?php $form=$this->beginWidget('CActiveForm', array(
	'id'=>'clients-form',
	// Please note: When you enable ajax validation, make sure the corresponding
	// controller action is handling ajax validation correctly.
	// There is a call to performAjaxValidation() commented in generated controller code.
	// See class documentation of CActiveForm for details on this.
	'enableAjaxValidation'=>false,
)); ?>

	<p class="note">Fields with <span class="required">*</span> are required.</p>

	<?php echo $form->errorSummary($model); ?>

	<div class="row">
		<?php echo $form->labelEx($model,'name'); ?>
		<?php echo $form->textField($model,'name',array('size'=>60,'maxlength'=>100)); ?>
		<?php echo $form->error($model,'name'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'designation'); ?>
		<?php echo $form->textField($model,'designation',array('size'=>60,'maxlength'=>100)); ?>
		<?php echo $form->error($model,'designation'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'house_number'); ?>
		<?php echo $form->textField($model,'house_number',array('size'=>20,'maxlength'=>20)); ?>
		<?php echo $form->error($model,'house_number'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'resident_number'); ?>
		<?php echo $form->textField($model,'resident_number'); ?>
		<?php echo $form->error($model,'resident_number'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'department'); ?>
		<?php echo $form->textField($model,'department',array('size'=>60,'maxlength'=>100)); ?>
		<?php echo $form->error($model,'department'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'hostel'); ?>
		<?php echo $form->textField($model,'hostel',array('size'=>50,'maxlength'=>50)); ?>
		<?php echo $form->error($model,'hostel'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'room_number'); ?>
		<?php echo $form->textField($model,'room_number',array('size'=>10,'maxlength'=>10)); ?>
		<?php echo $form->error($model,'room_number'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'contact_number'); ?>
		<?php echo $form->textField($model,'contact_number'); ?>
		<?php echo $form->error($model,'contact_number'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'complaint_type'); ?>
		<?php echo $form->textField($model,'complaint_type',array('size'=>60,'maxlength'=>100)); ?>
		<?php echo $form->error($model,'complaint_type'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'description'); ?>
		<?php echo $form->textArea($model,'description',array('rows'=>6, 'cols'=>50)); ?>
		<?php echo $form->error($model,'description'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'status'); ?>
		<?php echo $form->textField($model,'status',array('size'=>30,'maxlength'=>30)); ?>
		<?php echo $form->error($model,'status'); ?>
	</div>

	<div class="row buttons">
		<?php echo CHtml::submitButton($model->isNewRecord ? 'Create' : 'Save'); ?>
	</div>

<?php $this->endWidget(); ?>

</div><!-- form -->