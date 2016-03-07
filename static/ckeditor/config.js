/**
 * @license Copyright (c) 2003-2012, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
config.toolbar_Standard =
[

        { name: 'document',             items : [ 'Source','-','NewPage','Preview','DocProps',,'Print','-','Templates' ] },

        { name: 'clipboard',    items : [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ] },

        { name: 'editing',              items : [ 'Find','Replace','-','SelectAll'] },

        { name: 'links',                items : [ 'Link','Unlink'] },

        { name: 'paragraph',    items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','-',
                                            'JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'] },

        '/',

        { name: 'styles',               items : [ 'Styles','Format','Font','FontSize' ] },

        { name: 'colors',               items : [ 'TextColor','BGColor' ] },

        { name: 'basicstyles',  items : [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ] },

        { name: 'insert',               items : [ 'Image','Table','HorizontalRule','SpecialChar','PageBreak'] },

        { name: 'tools',       items : [ 'Maximize'] }

];

/*
[

	{ name: 'document',     items : [ 'NewPage','Preview','DocProps','Print','-','Templates' ] },

	{ name: 'clipboard',	items : [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ] },

	{ name: 'editing',	items : [ 'Find','Replace','-','SelectAll'] },

	{ name: 'links',	items : [ 'Link','Unlink'] },

	{ name: 'paragraph',	items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','-',
                                            'JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'] },

	'/',

	{ name: 'styles',	items : [ 'Styles','Format','Font','FontSize' ] },

	{ name: 'colors',	items : [ 'TextColor','BGColor' ] },

	{ name: 'basicstyles',	items : [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ] },

	{ name: 'insert',	items : [ 'Image','Table','HorizontalRule','SpecialChar','PageBreak'] },

        { name: 'tools',        items : [ 'Maximize'] }

];
*/

config.toolbar_BasicWithImage =
[
	{ name: 'basicstyles',	items : [ 'Bold','Italic','Underline'] },

	{ name: 'links',	items : [ 'Link','Unlink','Image'] },

	{ name: 'paragraph',	items : [ 'NumberedList','BulletedList','-','JustifyLeft','JustifyCenter','JustifyBlock'] },
];

config.toolbar_Basic =
[
	{ name: 'basicstyles',	items : [ 'Bold','Italic','Underline'] },

	{ name: 'links',	items : [ 'Link','Unlink'] },

];

//config.toolbar = 'BasicWithImage';
config.uiColor = '#fafafa';

//config.forcePasteAsPlainText = true;
config.pasteFromWordRemoveFontStyles = true;
config.pasteFromWordIgnoreFontFace = true;
config.pasteFromWordRemoveStyles = true;
config.pasteFromWordKeepsStructure = true;

};
