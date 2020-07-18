<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::group(['middleware' => ['cors']], function () {
    Route::get('/', function () {
        return 'Do U want to build a snow man?';
    });

    Route::get('/store', 'StoreController@list')->name('store.list');

    Route::get('/store/{id}', 'StoreController@index')->name('store.index');

    Route::post('/store', 'StoreController@sort')->name('store.sort');

    Route::post('/store/add', 'StoreController@add')->name('store.add');

    Route::get('/feedback/generate', 'FeedbackController@generate')->name('feedback.generate');
});
