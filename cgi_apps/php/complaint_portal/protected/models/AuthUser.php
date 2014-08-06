<?php

/**
 * This is the model class for table "auth_user".
 *
 * The followings are the available columns in table 'auth_user':
 * @property integer $id
 * @property string $username
 * @property string $first_name
 * @property string $last_name
 * @property string $email
 * @property string $password
 * @property integer $is_staff
 * @property integer $is_active
 * @property integer $is_superuser
 * @property string $last_login
 * @property string $date_joined
 *
 * The followings are the available model relations:
 * @property AuthMessage[] $authMessages
 * @property AuthUserGroups[] $authUserGroups
 * @property AuthUserUserPermissions[] $authUserUserPermissions
 * @property BirthdayBirthdaymessage[] $birthdayBirthdaymessages
 * @property BirthdayBirthdaymessage[] $birthdayBirthdaymessages1
 * @property BuysellBuymailssent[] $buysellBuymailssents
 * @property BuysellItemsforsale[] $buysellItemsforsales
 * @property BuysellItemsrequested[] $buysellItemsrequesteds
 * @property BuysellRequestmailssent[] $buysellRequestmailssents
 * @property DirectorspeechReply[] $directorspeechReplies
 * @property DjangoAdminLog[] $djangoAdminLogs
 * @property DjangoCommentFlags[] $djangoCommentFlags
 * @property DjangoComments[] $djangoComments
 * @property EbooksUploadinfo[] $ebooksUploadinfos
 * @property EventsCalendarUsers[] $eventsCalendarUsers
 * @property EventsEvent[] $eventsEvents
 * @property EventsEventsuser[] $eventsEventsusers
 * @property FacappFacspace $facappFacspace
 * @property FacappFaculty $facappFaculty
 * @property FeedModerationModeration[] $feedModerationModerations
 * @property GroupsGroup[] $groupsGroups
 * @property GroupsGroupinfoSubscribers[] $groupsGroupinfoSubscribers
 * @property HelpcenterReply[] $helpcenterReplies
 * @property HelpcenterResponse[] $helpcenterResponses
 * @property ImgWebsiteBlogpost[] $imgWebsiteBlogposts
 * @property ImgWebsiteRecentworks[] $imgWebsiteRecentworks
 * @property KritiItem[] $kritiItems
 * @property KritiKritiperson[] $kritiKritipeople
 * @property KritiPost[] $kritiPosts
 * @property LostfoundFounditems[] $lostfoundFounditems
 * @property LostfoundLostitems[] $lostfoundLostitems
 * @property NotificationsNotificationuser $notificationsNotificationuser
 * @property NucleusFeatureVisitedUsers[] $nucleusFeatureVisitedUsers
 * @property NucleusPerson $nucleusPerson
 * @property ThinktankProfile $thinktankProfile
 * @property UtilitiesEmailauthuser $utilitiesEmailauthuser
 * @property UtilitiesTheme $utilitiesTheme
 * @property UtilitiesUsersession[] $utilitiesUsersessions
 * @property WebtoolCollege $webtoolCollege
 * @property WebtoolInfo $webtoolInfo
 * @property WebtoolSchool $webtoolSchool
 * @property Wifimac[] $wifimacs
 */
class AuthUser extends CActiveRecord
{
	/**
	 * @return string the associated database table name
	 */
	public function tableName()
	{
		return 'auth_user';
	}

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined', 'required'),
			array('is_staff, is_active, is_superuser', 'numerical', 'integerOnly'=>true),
			array('username, first_name, last_name', 'length', 'max'=>30),
			array('email', 'length', 'max'=>75),
			array('password', 'length', 'max'=>128),
			// The following rule is used by search().
			// @todo Please remove those attributes that should not be searched.
			array('id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined', 'safe', 'on'=>'search'),
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
			'authMessages' => array(self::HAS_MANY, 'AuthMessage', 'user_id'),
			'authUserGroups' => array(self::HAS_MANY, 'AuthUserGroups', 'user_id'),
			'authUserUserPermissions' => array(self::HAS_MANY, 'AuthUserUserPermissions', 'user_id'),
			'birthdayBirthdaymessages' => array(self::HAS_MANY, 'BirthdayBirthdaymessage', 'receiver_id'),
			'birthdayBirthdaymessages1' => array(self::HAS_MANY, 'BirthdayBirthdaymessage', 'sender_id'),
			'buysellBuymailssents' => array(self::HAS_MANY, 'BuysellBuymailssent', 'by_user_id'),
			'buysellItemsforsales' => array(self::HAS_MANY, 'BuysellItemsforsale', 'user_id'),
			'buysellItemsrequesteds' => array(self::HAS_MANY, 'BuysellItemsrequested', 'user_id'),
			'buysellRequestmailssents' => array(self::HAS_MANY, 'BuysellRequestmailssent', 'by_user_id'),
			'directorspeechReplies' => array(self::HAS_MANY, 'DirectorspeechReply', 'user_id'),
			'djangoAdminLogs' => array(self::HAS_MANY, 'DjangoAdminLog', 'user_id'),
			'djangoCommentFlags' => array(self::HAS_MANY, 'DjangoCommentFlags', 'user_id'),
			'djangoComments' => array(self::HAS_MANY, 'DjangoComments', 'user_id'),
			'ebooksUploadinfos' => array(self::HAS_MANY, 'EbooksUploadinfo', 'user_id'),
			'eventsCalendarUsers' => array(self::HAS_MANY, 'EventsCalendarUsers', 'user_id'),
			'eventsEvents' => array(self::HAS_MANY, 'EventsEvent', 'uploader_id'),
			'eventsEventsusers' => array(self::HAS_MANY, 'EventsEventsuser', 'user_id'),
			'facappFacspace' => array(self::HAS_ONE, 'FacappFacspace', 'user_id'),
			'facappFaculty' => array(self::HAS_ONE, 'FacappFaculty', 'user_id'),
			'feedModerationModerations' => array(self::HAS_MANY, 'FeedModerationModeration', 'moderator_id'),
			'groupsGroups' => array(self::HAS_MANY, 'GroupsGroup', 'user_id'),
			'groupsGroupinfoSubscribers' => array(self::HAS_MANY, 'GroupsGroupinfoSubscribers', 'user_id'),
			'helpcenterReplies' => array(self::HAS_MANY, 'HelpcenterReply', 'user_id'),
			'helpcenterResponses' => array(self::HAS_MANY, 'HelpcenterResponse', 'user_id'),
			'imgWebsiteBlogposts' => array(self::HAS_MANY, 'ImgWebsiteBlogpost', 'author_id'),
			'imgWebsiteRecentworks' => array(self::HAS_MANY, 'ImgWebsiteRecentworks', 'author_id'),
			'kritiItems' => array(self::HAS_MANY, 'KritiItem', 'user_id'),
			'kritiKritipeople' => array(self::HAS_MANY, 'KritiKritiperson', 'user_id'),
			'kritiPosts' => array(self::HAS_MANY, 'KritiPost', 'user_id'),
			'lostfoundFounditems' => array(self::HAS_MANY, 'LostfoundFounditems', 'user_id'),
			'lostfoundLostitems' => array(self::HAS_MANY, 'LostfoundLostitems', 'user_id'),
			'notificationsNotificationuser' => array(self::HAS_ONE, 'NotificationsNotificationuser', 'user_id'),
			'nucleusFeatureVisitedUsers' => array(self::HAS_MANY, 'NucleusFeatureVisitedUsers', 'user_id'),
			'nucleusPerson' => array(self::HAS_ONE, 'NucleusPerson', 'user_id'),
			'thinktankProfile' => array(self::HAS_ONE, 'ThinktankProfile', 'user_id'),
			'utilitiesEmailauthuser' => array(self::HAS_ONE, 'UtilitiesEmailauthuser', 'user_id'),
			'utilitiesTheme' => array(self::HAS_ONE, 'UtilitiesTheme', 'user_id'),
			'utilitiesUsersessions' => array(self::HAS_MANY, 'UtilitiesUsersession', 'user_id'),
			'webtoolCollege' => array(self::HAS_ONE, 'WebtoolCollege', 'user_id'),
			'webtoolInfo' => array(self::HAS_ONE, 'WebtoolInfo', 'user_id'),
			'webtoolSchool' => array(self::HAS_ONE, 'WebtoolSchool', 'user_id'),
			'wifimacs' => array(self::HAS_MANY, 'Wifimac', 'enrol'),
		);
	}

	/**
	 * @return array customized attribute labels (name=>label)
	 */
	public function attributeLabels()
	{
		return array(
			'id' => 'ID',
			'username' => 'Username',
			'first_name' => 'First Name',
			'last_name' => 'Last Name',
			'email' => 'Email',
			'password' => 'Password',
			'is_staff' => 'Is Staff',
			'is_active' => 'Is Active',
			'is_superuser' => 'Is Superuser',
			'last_login' => 'Last Login',
			'date_joined' => 'Date Joined',
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
		$criteria->compare('username',$this->username,true);
		$criteria->compare('first_name',$this->first_name,true);
		$criteria->compare('last_name',$this->last_name,true);
		$criteria->compare('email',$this->email,true);
		$criteria->compare('password',$this->password,true);
		$criteria->compare('is_staff',$this->is_staff);
		$criteria->compare('is_active',$this->is_active);
		$criteria->compare('is_superuser',$this->is_superuser);
		$criteria->compare('last_login',$this->last_login,true);
		$criteria->compare('date_joined',$this->date_joined,true);

		return new CActiveDataProvider($this, array(
			'criteria'=>$criteria,
		));
	}

	/**
	 * Returns the static model of the specified AR class.
	 * Please note that you should have this exact method in all your CActiveRecord descendants!
	 * @param string $className active record class name.
	 * @return AuthUser the static model class
	 */
	public static function model($className=__CLASS__)
	{
		return parent::model($className);
	}
}
