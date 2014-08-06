<?php

/**
 * This is the model class for table "ocp_clients".
 *
 * The followings are the available columns in table 'ocp_clients':
 * @property integer $id
 * @property string $name
 * @property string $designation
 * @property string $house_number
 * @property integer $resident_number
 * @property string $department
 * @property string $hostel
 * @property string $room_number
 * @property integer $contact_number
 * @property string $complaint_type
 * @property string $description
 * @property string $status
 */
class Clients extends CActiveRecord
{
	/**
	 * @return string the associated database table name
	 */
	public function tableName()
	{
		return 'ocp_clients';
	}

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('resident_number, contact_number', 'numerical', 'integerOnly'=>true),
			array('name, designation, department, complaint_type', 'length', 'max'=>100),
			array('house_number', 'length', 'max'=>20),
			array('hostel', 'length', 'max'=>50),
			array('room_number', 'length', 'max'=>10),
			array('status', 'length', 'max'=>30),
			array('description', 'safe'),
      array('name, contact_number, complaint_type, description, status', 'required'),
			// The following rule is used by search().
			// @todo Please remove those attributes that should not be searched.
			array('id, name, designation, house_number, resident_number, department, hostel, room_number, contact_number, complaint_type, description, status', 'safe', 'on'=>'search'),
		);
	}

	/**
	 * @return array relational rules.
	 */
	public function relations()
	{
		// NOTE: you may need to adjust the relation name and the related
		// class name for the relations automatically generated below.
		return array(
		);
	}

	/**
	 * @return array customized attribute labels (name=>label)
	 */
	public function attributeLabels()
	{
		return array(
			'id' => 'ID',
			'name' => 'Name',
			'designation' => 'Designation',
			'house_number' => 'House Number',
			'resident_number' => 'Resident Number',
			'department' => 'Department',
			'hostel' => 'Hostel',
			'room_number' => 'Room Number',
			'contact_number' => 'Contact Number',
			'complaint_type' => 'Complaint Type',
			'description' => 'Description',
			'status' => 'Status',
		);
	}

	/**
	 * Retrieves a list of models based on the current search/filter conditions.
	 *
	 * Typical usecase:
	 * - Initialize the model fields with values from filter form.
	 * - Execute this method to get CActiveDataProvider instance which will filter
	 * models according to data in model fields.
	 * - Pass data provider to CGridView, CListView or any similar widget.
	 *
	 * @return CActiveDataProvider the data provider that can return the models
	 * based on the search/filter conditions.
	 */
	public function search()
	{
		// @todo Please modify the following code to remove attributes that should not be searched.

		$criteria=new CDbCriteria;

		$criteria->compare('id',$this->id);
		$criteria->compare('name',$this->name,true);
		$criteria->compare('designation',$this->designation,true);
		$criteria->compare('house_number',$this->house_number,true);
		$criteria->compare('resident_number',$this->resident_number);
		$criteria->compare('department',$this->department,true);
		$criteria->compare('hostel',$this->hostel,true);
		$criteria->compare('room_number',$this->room_number,true);
		$criteria->compare('contact_number',$this->contact_number);
		$criteria->compare('complaint_type',$this->complaint_type,true);
		$criteria->compare('description',$this->description,true);
		$criteria->compare('status',$this->status,true);

		return new CActiveDataProvider($this, array(
			'criteria'=>$criteria,
		));
	}

	/**
	 * Returns the static model of the specified AR class.
	 * Please note that you should have this exact method in all your CActiveRecord descendants!
	 * @param string $className active record class name.
	 * @return Clients the static model class
	 */
	public static function model($className=__CLASS__)
	{
		return parent::model($className);
	}
}
