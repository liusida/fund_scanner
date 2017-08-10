IPython.toolbar.add_buttons_group([
        {
             'label'   : 'kill and run-all',
             'icon'    : 'fa fa-angle-double-down',
             'callback': function(){
                 IPython.notebook.kernel.restart();
                 setTimeout(function(){
                     IPython.notebook.execute_all_cells();
                 }, 1000);
             }
        }
    ]);