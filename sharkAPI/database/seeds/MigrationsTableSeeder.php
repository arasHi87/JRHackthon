<?php

use Illuminate\Database\Seeder;

class MigrationsTableSeeder extends Seeder
{

    /**
     * Auto generated seed file
     *
     * @return void
     */
    public function run()
    {
        

        \DB::table('migrations')->delete();
        
        \DB::table('migrations')->insert(array (
            0 => 
            array (
                'id' => 1,
                'migration' => '2020_07_18_143503_create_stores_table',
                'batch' => 1,
            ),
            1 => 
            array (
                'id' => 4,
                'migration' => '2020_07_18_211413_create_feedbacks_table',
                'batch' => 2,
            ),
        ));
        
        
    }
}