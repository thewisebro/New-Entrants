package img.myapplication;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;

import models.StudentModel;


public class Update extends ActionBarActivity {

    private Spinner state;
    private EditText name;
    private EditText username;
    private EditText branch;
    private EditText town;
    private EditText mobile;
    private EditText email;
    private EditText fblink;
    private StudentModel student;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_update);
        student= (StudentModel) getIntent().getSerializableExtra("student");

        setViews();
        setInitial();

    }
    private void setViews(){
        name= (EditText) findViewById(R.id.u_name);
        username= (EditText) findViewById(R.id.u_username);
        town= (EditText) findViewById(R.id.u_town);
        branch= (EditText) findViewById(R.id.u_branch);
        mobile= (EditText) findViewById(R.id.u_mobile);
        email= (EditText) findViewById(R.id.u_email);
        fblink= (EditText) findViewById(R.id.u_fblink);

        state= (Spinner) findViewById(R.id.u_state);
        ArrayAdapter<CharSequence> stateList=ArrayAdapter.createFromResource(this,R.array.states,android.R.layout.simple_spinner_item);
        stateList.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        state.setAdapter(stateList);
    }
    private void setInitial(){

            name.setText(student.name);
            username.setText(student.username);
            branch.setText(student.branchname);
            mobile.setText(student.mobile);
            email.setText(student.email);
            fblink.setText(student.fb_link);
            town.setText(student.town);
            state.setSelection(getSpinnerPos(student.statecode));
    }
    private int getSpinnerPos(String state){
        String[] list= getResources().getStringArray(R.array.state_codes);
        for (int i=0;i<list.length;i++)
            if (list[i].equals(state.toCharArray()))
                return i;
        return -1;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_update, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
