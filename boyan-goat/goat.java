package telebid;
import java.util.*;
public class Goat {
    ///sloji ogranicheniq
    public static void main(String[] args){
        int maxBroiKursove=0;
        int broiKozichki=0;
        int kapacitetNaSal=0;
        Scanner sc = new Scanner(System.in);
   
        //    System.out.println("Vuvedi broi kozichki");
        while(broiKozichki<1 || broiKozichki>1000){
          broiKozichki = sc.nextInt();
        }
        //      System.out.println("Vuvedi jelan maksimalen broi kursove");
        while(maxBroiKursove<1||maxBroiKursove>1000){
        maxBroiKursove = sc.nextInt();
        }
        int teglo[] = new int[broiKozichki+1]; //priemame che tegloto e cqlo chislo
        int secondarrp[] =new int[broiKozichki+1];      //pazim ednakuv masiv za da moje da zanulqvame promenlivite v purviq
        int sumaOtTegla=0;                  //izpolzvame q za daizbegnem izlishni proverki
        
        for(int counter=0;counter<broiKozichki;counter++){
           System.out.println("Vuvedete tegloto za koza nomer: "+counter);
           teglo[counter]=sc.nextInt();           
           while(teglo[counter]<1||teglo[counter]>10000000){ 
                          teglo[counter]=sc.nextInt();
           }        
            secondarrp[counter]=teglo[counter];
            sumaOtTegla+=teglo[counter];
        }
       Arrays.sort(teglo); //podrejda gi po vuzhodqsht red    
       Arrays.sort(secondarrp);
      double d = (double)sumaOtTegla/(double)maxBroiKursove;
       kapacitetNaSal= sumaOtTegla/maxBroiKursove; //pravim kapaciteta na sala da e minimum srednoto teglo deleno na jelaniq broi prevozi  
      // if((d%2)!=0){ //ako e nechetno moje da spestim oshte 1 proverka
        //   kapacitetNaSal++;
       //}
     boolean uslovie=false;         //Da uspee da kachi vsichki v zadadeniq ot nas broi kursove
     int zaetoTegloVSala=0;
     int counter2=0;            //pazi ni poslednata izpolzvana kozichka (ne e nujna kato cqlo)
     int counter=broiKozichki;      //izpolzva se za obhojdane na masiva
     int tekushtBroiPrevozi=1;
     int suma=0;
     int nai_malka=teglo[broiKozichki];
     while(!(uslovie)){
           while(counter>0){
               if(!(teglo[counter]+zaetoTegloVSala>kapacitetNaSal)&&teglo[counter]!=0){
                   //imame mqsto v sala
                   if(teglo[counter]+zaetoTegloVSala<=kapacitetNaSal){
                   zaetoTegloVSala+=teglo[counter]; 
                                      System.out.println("going to use "+teglo[counter]+" on try: "+tekushtBroiPrevozi);
                   teglo[counter]=0;
                   }
                   for(int i=0;i<teglo.length;i++){
                       if(teglo[i]<nai_malka&&teglo[i]!=0){
                        nai_malka=teglo[i];
                       }
                   }
                 //  System.out.println("salut teji:"+zaetoTegloVSala);
               }
               else{
                   System.out.println("entered firstl else current teglo[counter] is "+teglo[counter]+"secondarrp[counter] is"+secondarrp[counter]+"counter is "+counter);
               }
                
               if(nai_malka+zaetoTegloVSala>kapacitetNaSal) //ako nqma mqsto dori i za nai-malkata kozichka(za da izbegnem izlishni proverk)
                       {
                counter2=broiKozichki;    //poslednata izpolzvana kozichka
                counter=0;                
                   }                          
               counter--;
                   }
         for(int i=0;i<teglo.length;i++){
                       suma+=teglo[i];
                   }
                                      if(suma==0 && tekushtBroiPrevozi==maxBroiKursove){            //ako sme uspeli da izpulnim uslovieto
               System.out.println("sal:" +kapacitetNaSal +"tekprevozi i maxborikursove"+tekushtBroiPrevozi + maxBroiKursove);
                              uslovie=true;
           }
         tekushtBroiPrevozi++;
           if(tekushtBroiPrevozi>maxBroiKursove){           //ako ne sme uspeliu da izpulnim uslovieto
               tekushtBroiPrevozi=1;
               System.out.println("in this if");
               kapacitetNaSal++;                           //uvelichavame minimalniq nujen s kapacitet s 1
               counter2=broiKozichki;
for (int ida=0;ida<broiKozichki+1;ida++){
    teglo[ida]=secondarrp[ida];
}
        }
           
           if(suma==0){
for (int ida=0;ida<broiKozichki+1;ida++){
    teglo[ida]=secondarrp[ida];
}           }
           zaetoTegloVSala=0;                           //"restartirame" nujnite promenlivi
           counter=counter2;
           counter2=0;
            nai_malka=secondarrp[broiKozichki];
            suma=0;
            zaetoTegloVSala=0;
     counter=broiKozichki;      //izpolzva se za obhojdane na masiva
                    System.out.println("reached end");

}           
 }
}
