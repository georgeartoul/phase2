package GUI;

import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.URL;
import java.util.ResourceBundle;

import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.Spinner;
import javafx.scene.control.SpinnerValueFactory;
import javafx.scene.control.SplitPane;

public class SimulatedTrafficController implements Initializable {

	
	public static Stage primaryStage;
	FileWriter fw = null;
	BufferedWriter bw = null;
	PrintWriter pw = null;
	
	SpinnerValueFactory<Double> sp11 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);
	SpinnerValueFactory<Double> sp12 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);
	SpinnerValueFactory<Double> sp13 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);
	
	SpinnerValueFactory<Double> sp21 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);
	SpinnerValueFactory<Double> sp22 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);
	SpinnerValueFactory<Double> sp23 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);

	SpinnerValueFactory<Double> sp31 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);
	SpinnerValueFactory<Double> sp32 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);
	SpinnerValueFactory<Double> sp33 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);

	SpinnerValueFactory<Double> sp41 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);
	SpinnerValueFactory<Double> sp42 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);
	SpinnerValueFactory<Double> sp43 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);

	SpinnerValueFactory<Double> sp51 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);
	SpinnerValueFactory<Double> sp52 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);
	SpinnerValueFactory<Double> sp53 = new SpinnerValueFactory.DoubleSpinnerValueFactory(0, 100, 0);
	
	  @FXML
	    private SplitPane sPane;

	    @FXML
	    private Spinner<Double> g1p1;

	    @FXML
	    private Button backBtn;

	    @FXML
	    private Button nextBtn;

	    @FXML
	    private Spinner<Double> g1p2;

	    @FXML
	    private Spinner<Double> g2p1;

	    @FXML
	    private Spinner<Double> g2p2;

	    @FXML
	    private Spinner<Double> g2p3;

	    @FXML
	    private Spinner<Double> g1p3;

	    @FXML
	    private Spinner<Double> g5p3;

	    @FXML
	    private Spinner<Double> g5p2;

	    @FXML
	    private Spinner<Double> g5p1;

	    @FXML
	    private Spinner<Double> g4p3;

	    @FXML
	    private Spinner<Double> g4p2;

	    @FXML
	    private Spinner<Double> g4p1;

	    @FXML
	    private Spinner<Double> g3p3;

	    @FXML
	    private Spinner<Double> g3p2;

	    @FXML
	    private Spinner<Double> g3p1;

	    @FXML
	    void backStep(ActionEvent event) throws Exception {
	    	
	    	EnterParamsController enterParametersWindow = new EnterParamsController();
	    	enterParametersWindow.start(primaryStage);

	    }

	    @FXML
	    void nextStep(ActionEvent event) throws IOException {
	    /*	if(g1p1.getValue() + g2p1.getValue()>100 || g3p1.getValue() + g4p1.getValue() +
	    			g5p1.getValue()>100
	    			|| g1p2.getValue()+g1p3.getValue()!=100 || g2p2.getValue()+g2p3.getValue()!=100
	    			|| g3p2.getValue()+g3p3.getValue()!=100 || g4p2.getValue()+g4p3.getValue()!=100
	    			|| g5p2.getValue()+g5p3.getValue()!=100)
	    		Platform.runLater(new Runnable() {
	    			@Override
	    			public void run() {
	    				Alert alert = new Alert(AlertType.ERROR);
	    				alert.setHeaderText("Error in the values!");
	    				alert.show(); 
	    			}
	    		});
	    	else {*/
				
			
	    	fw = new FileWriter("C:\\Users\\franc\\eclipse-workspace\\Phase2\\src\\GUI\\DataBase.txt", true);
			bw = new BufferedWriter(fw);
			pw = new PrintWriter(bw);
			pw.println(g1p1.getValue()+","+g1p2.getValue()+","+g1p3.getValue());
			pw.println(g2p1.getValue()+","+g2p2.getValue()+","+g2p3.getValue());
			pw.println(g3p1.getValue()+","+g3p2.getValue()+","+g3p3.getValue());
			pw.println(g4p1.getValue()+","+g4p2.getValue()+","+g4p3.getValue());
			pw.println(g5p1.getValue()+","+g5p2.getValue()+","+g5p3.getValue());
			pw.flush();	
	    	//}
	    	
	    	SetStrategyController setStrategyController = new SetStrategyController();
	    	setStrategyController.start(primaryStage);
	    	
	    }
	    


	
	
	 public void start(Stage primaryStage) {
			SimulatedTrafficController.primaryStage = primaryStage;
			try {
				SimulatedTrafficController.primaryStage = primaryStage;
				Parent root;
				root = FXMLLoader.load(getClass().getResource("SimulatedTrafficDetails.fxml"));
				Scene scene = new Scene(root);
				SimulatedTrafficController.primaryStage.setScene(scene);
				SimulatedTrafficController.primaryStage.setTitle("Traffic Details");
				SimulatedTrafficController.primaryStage.show();
				SimulatedTrafficController.primaryStage.setOnCloseRequest(event -> {
					System.exit(0);
				});
			} catch (Exception e) {
				e.printStackTrace();
			}

		}


	@Override
	public void initialize(URL arg0, ResourceBundle arg1) {
		// TODO Auto-generated method stub
		g1p1.setValueFactory(sp11);
		g1p2.setValueFactory(sp12);
		g1p3.setValueFactory(sp13);
		g2p1.setValueFactory(sp21);
		g2p2.setValueFactory(sp22);
		g2p3.setValueFactory(sp23);
		g3p1.setValueFactory(sp31);
		g3p2.setValueFactory(sp32);
		g3p3.setValueFactory(sp33);
		g4p1.setValueFactory(sp41);
		g4p2.setValueFactory(sp42);
		g4p3.setValueFactory(sp43);
		g5p1.setValueFactory(sp51);
		g5p2.setValueFactory(sp52);
		g5p3.setValueFactory(sp53);

		
	}
	
}
