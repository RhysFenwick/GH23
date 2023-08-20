import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DonorDashboardComponent } from './donor-dashboard/donor-dashboard.component';
import { AdminDashboardComponent } from './admin-dashboard/admin-dashboard.component';
import { OrgDashboardComponent } from './org-dashboard/org-dashboard.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'donors',
    pathMatch: 'full',
  },
  {
    path: 'donors',
    component: DonorDashboardComponent,
  },
  {
    path: 'admin',
    component: AdminDashboardComponent,
  },
  {
    path: 'org',
    component: OrgDashboardComponent,
  },
  {
    path: '*',
    redirectTo: 'donors',
    pathMatch: 'full',
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
