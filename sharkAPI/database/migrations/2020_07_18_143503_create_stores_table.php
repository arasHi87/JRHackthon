<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateStoresTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('stores', function (Blueprint $table) {
            $table->id();
            $table->string('name')->comment('商家名稱');
            $table->string('address')->comment('商家地址');
            $table->integer('rating')->comment('商家評分');
            $table->longtext('image')->comment('商家圖片網址');
            $table->double('longitude')->comment('經度');
            $table->double('latitude')->comment('緯度');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('stores');
    }
}
